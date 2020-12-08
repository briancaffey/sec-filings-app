import decimal
import logging

from django.shortcuts import render
from django.db.models import (
    Avg,
    F,
    Q,
    Sum,
    StdDev,
    Count,
    Max,
    Min,
    ExpressionWrapper,
    FloatField,
)

from django.http import HttpResponse, JsonResponse
from django.views.decorators.cache import cache_page

# Create your views here.
from rest_framework import status, viewsets
from rest_framework.decorators import api_view
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework import serializers


from .models import Filing, FilingList, Holding, Cik, Cusip
from .serializers import (
    DetailCusipSerializer,
    BaseCusipSerializer,
    CikSerializer,
    CiksByCusipSerializer,
    HistoricalCusipSerializer,
    CusipSerializer,
    FilingPeriodSerializer,
    FilingSerializer,
    FundScatterplotSerializer,
    HistoricalPortfolioValueSerializer,
    HoldingSerializer,
    HoldingGraphSerializer,
    HoldingHistoricalSerializer,
    PortfolioByPeriodSerializer,
)


logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


class FilingPeriods(viewsets.ViewSet):
    def get(self, request):
        periods = FilingList.objects.all().exclude(datafile="").order_by("quarter")
        serializer = FilingPeriodSerializer(periods, many=True)
        return Response(serializer.data)


class FilingViewSet(viewsets.ViewSet):
    paginator = LimitOffsetPagination()

    def get(self, request):
        filings = Filing.objects.all()
        if search := request.GET.get("search"):
            filings = filings.filter(
                Q(cik__filer_name__icontains=search)
                | Q(cik__cik_number__icontains=search)
            )

        filings = filings.annotate(total_value=Sum("filing__value")).values(
            "total_value",
            "form_type",
            "date_filed",
            "filename",
            "datafile",
            "cik__cik_number",
            "cik__filer_name",
        )

        if sorting := request.GET.get("sorting"):
            filings = filings.order_by(sorting)

        filings = result_page = self.paginator.paginate_queryset(filings, request)
        serializer = FilingSerializer(result_page, many=True)
        return_data = self.paginator.get_paginated_response(serializer.data)
        return return_data


class HoldingViewSet(viewsets.ViewSet):
    paginator = LimitOffsetPagination()

    def get(self, request):
        holdings = Holding.objects.all().prefetch_related(
            "filing__cik", "cusip", "filing__filing_list"
        )
        if sorting := request.GET.get("sorting"):
            holdings = holdings.order_by(sorting)
        if search := request.GET.get("search"):
            holdings = holdings.filter(
                Q(nameOfIssuer__icontains=search)
                | Q(cusip__cusip_number__icontains=search)
            )
        result_page = self.paginator.paginate_queryset(holdings, request)
        serializer = HoldingSerializer(result_page, many=True)
        return_data = self.paginator.get_paginated_response(serializer.data)
        return return_data

    def holdings_by_cik(self, request, cik):

        top_holdings = (
            Holding.objects.filter(filing__cik=cik)
            .values("cusip", "nameOfIssuer")
            .annotate(total=Sum("value"))
        )

        top_holdings = top_holdings.order_by("-total")

        # get all holdings
        self.paginator.default_limit = top_holdings.count()

        result_page = self.paginator.paginate_queryset(top_holdings, request)
        serializer = HoldingGraphSerializer(result_page, many=True)
        return_data = self.paginator.get_paginated_response(serializer.data)
        return return_data

    def historical_holdings_by_cik(self, request, cik, cusip):
        cik = Cik.objects.get(cik_number=cik)
        cusip = Cusip.objects.get(cusip_number=cusip)

        historical_holdings = (
            Holding.objects.filter(filing__cik=cik, cusip=cusip)
            .values("filing__date_filed")
            .annotate(sshPrnamt=Sum("sshPrnamt"), value=Sum("value"))
            .values(
                "filing__date_filed",
                "sshPrnamt",
                "value",
                "cusip__cusip_number",
                "cusip__company_name",
                "filing__cik__cik_number",
                "filing__cik__filer_name",
            )
            .order_by("filing__date_filed")
        )

        # self.paginator.default_limit = historical_holdings.count()
        # result_page = self.paginator.paginate_queryset(historical_holdings, request)
        data = {}
        serializer = HoldingHistoricalSerializer(historical_holdings, many=True)
        data["results"] = serializer.data
        data["company_name"] = cik.filer_name
        # return_data = self.paginator.get_paginated_response(serializer.data)
        # return_data = return_data.data.update({"updated": "updte"})
        return Response(data)


class CusipViewSet(viewsets.ViewSet):
    paginator = LimitOffsetPagination()

    def cusip_list(self, request):
        cusips = Cusip.objects.all()

        if search := request.GET.get("search"):
            cusips = cusips.filter(
                Q(company_name__icontains=search) | Q(cusip_number__icontains=search)
            )

        cusips = cusips.annotate(
            held_by_funds=Sum("cusip__value"), holding_count=Count("cusip")
        ).values("held_by_funds", "holding_count", "cusip_number", "company_name", "id")

        if sorting := request.GET.get("sorting"):
            cusips = cusips.order_by(sorting)

        result_page = self.paginator.paginate_queryset(cusips, request)
        serializer = CusipSerializer(result_page, many=True)
        return_data = self.paginator.get_paginated_response(serializer.data)
        return return_data

    def get(self, request, cusip, **kwargs):
        cusip_object = Cusip.objects.get(cusip_number=cusip)

        # how many investors hold this security in the current period
        current_period_holdings = Holding.objects.filter(
            cusip=cusip_object, filing__filing_list=request.period
        )

        held_by = current_period_holdings.count()

        total_shares = current_period_holdings.aggregate(
            total_shares=Sum("sshPrnamt")
        ).get("total_shares")

        total_value = (
            Holding.objects.filter(cusip=cusip_object)
            .aggregate(total_value=Sum("value"))
            .get("total_value")
        )

        average_value = 1000 * total_value / total_shares

        serializer = DetailCusipSerializer(
            cusip_object, context={"average_value": average_value, "held_by": held_by}
        )
        return Response(serializer.data)

    def cik_by_cusip(self, request, cusip, **kwargs):
        """
        Show all Investors that hold a security (CUSIP)
        with details for each investor including:
            - first Quarter held
            - Current period total value and total total_shares
            - cik number / filing name
        """

        cusip = Cusip.objects.get(cusip_number=cusip)

        # get filing_ciks from holdings
        filings_from_holdings = Holding.objects.filter(cusip=cusip).values_list(
            "filing", flat=True
        )

        # ciks from filings
        ciks_from_filings = Filing.objects.filter(
            cik__in=filings_from_holdings, filing_list=request.period
        ).values_list("cik", flat=True)

        cusip_filter = Q(filing_cik__filing__cusip=cusip)

        ciks = (
            Cik.objects.filter(id__in=ciks_from_filings)
            .prefetch_related("filing_cik", "filing_cik__filing_list")
            .annotate(
                total_portfolio_value=Sum("filing_cik__filing__value"),
                total_value=Sum("filing_cik__filing__value", filter=cusip_filter),
                total_shares=Sum("filing_cik__filing__sshPrnamt", filter=cusip_filter),
                first_filed=Min("filing_cik__filing_list__quarter"),
                percent_of_portfolio=ExpressionWrapper(
                    F("total_value") / F("total_portfolio_value"),
                    output_field=FloatField(),
                ),
            )
            .values(
                "total_value",
                "total_shares",
                "cik_number",
                "filer_name",
                "first_filed",
                "percent_of_portfolio",
            )
        )

        serializer = CiksByCusipSerializer(ciks, many=True)

        return Response(serializer.data)

    def historical_cusip_average_price(self, request, cusip, **kwargs):
        """
        Calculate the average price of a security per quarter
        by dividing the total sum of all holdings for a CUSIP
        by the total number of shares reported by all filers
        """

        cusip = Cusip.objects.get(cusip_number=cusip)

        cusip_filter = Q(filinglist__filing__cusip=cusip)

        historical_prices = (
            FilingList.objects.all()
            .annotate(
                sum_of_value=Sum(
                    "filinglist__filing__value",
                    filter=cusip_filter,
                ),
                sum_of_shares=Sum(
                    "filinglist__filing__sshPrnamt",
                    filter=cusip_filter,
                ),
                total_holdings=Count("filinglist__filing", filter=cusip_filter),
                average_value=ExpressionWrapper(
                    1000 * F("sum_of_value") / F("sum_of_shares"),
                    output_field=FloatField(),
                ),
            )
            .values(
                "sum_of_value",
                "sum_of_shares",
                "average_value",
                "total_holdings",
                "quarter",
            )
            .order_by("-quarter")
        )

        serializer = HistoricalCusipSerializer(historical_prices, many=True)

        return Response(serializer.data)


class CikViewSet(viewsets.ViewSet):
    paginator = LimitOffsetPagination()

    def cik_list(self, request, **kwargs):

        ciks = (
            Cik.objects.all()
            .annotate(
                current_period_holding_count=Count(
                    "filing_cik__filing",
                    filter=Q(filing_cik__filing_list=request.period),
                ),
                current_period_fund_size=Sum(
                    "filing_cik__filing__value",
                    filter=Q(filing_cik__filing_list=request.period),
                ),
                total_periods_filed=Count("filing_cik__filing_list__id", distinct=True),
            )
            .values(
                "current_period_holding_count",
                "current_period_fund_size",
                "cik_number",
                "filer_name",
                "total_periods_filed",
            )
        )

        if sorting := request.GET.get("sorting"):
            ciks = ciks.order_by(sorting)
        else:
            ciks = ciks.order_by(
                "-total_periods_filed", "-current_period_holding_count"
            )

        if search := request.GET.get("search"):
            ciks = ciks.filter(
                Q(filer_name__icontains=search) | Q(cik_number__icontains=search)
            )

        result_page = self.paginator.paginate_queryset(ciks, request)
        serializer = CikSerializer(result_page, many=True)
        return_data = self.paginator.get_paginated_response(serializer.data)
        return return_data

    # todo: this should be FilingList, not filing
    def historical_portfolio_value(self, request, cik):
        cik = Cik.objects.get(cik_number=cik)
        historical_values = (
            Filing.objects.filter(cik__cik_number=cik.cik_number)
            .values("filing_list__quarter")
            .annotate(value=Sum("filing__value"))
            .values("filing_list__quarter", "value")
            .order_by("-filing_list__quarter")
        )

        self.paginator.default_limit = historical_values.count()
        result_page = self.paginator.paginate_queryset(historical_values, request)
        serializer = HistoricalPortfolioValueSerializer(result_page, many=True)

        return_data = self.paginator.get_paginated_response(serializer.data)

        return return_data

    def portfolio_by_period(self, request, cik, **kwargs):
        cik = Cik.objects.get(cik_number=cik)
        holdings = Holding.objects.filter(
            filing__cik=cik, filing__filing_list=request.period
        )
        previous_period_holdings = Holding.objects.filter(
            filing__cik=cik, filing__filing_list=request.period.previous_filing_list()
        )

        previous_period_total_portfolio_value = previous_period_holdings.aggregate(
            Sum("value")
        )["value__sum"]
        total_portfolio_value = holdings.aggregate(Sum("value"))["value__sum"]

        previous_period_portfolio_holdings_by_value = (
            previous_period_holdings.values("cusip", "nameOfIssuer")
            .annotate(
                total=Sum("value"),
                percentage=Sum("value") / previous_period_total_portfolio_value,
                total_shares=Sum("sshPrnamt"),
            )
            .values("cusip", "nameOfIssuer", "total", "percentage", "sshPrnamt")
            .order_by("-total")
        )

        portfolio_holdings_by_value = (
            holdings.values("cusip", "nameOfIssuer", "sshPrnamtType")
            .annotate(
                total=Sum("value"),
                percentage=Sum("value") / total_portfolio_value,
                total_shares=Sum("sshPrnamt"),
            )
            .values(
                "cusip__cusip_number",
                "cusip__company_name",
                "nameOfIssuer",
                "total",
                "percentage",
                "sshPrnamt",
                "sshPrnamtType",
            )
            .order_by("-total")
        )

        if search := request.GET.get("search"):
            portfolio_holdings_by_value = portfolio_holdings_by_value.filter(
                nameOfIssuer__icontains=search
            )

        if sorting := request.GET.get("sorting"):
            portfolio_holdings_by_value = portfolio_holdings_by_value.order_by(sorting)

        self.paginator.default_limit = portfolio_holdings_by_value.count()

        if chart := request.GET.get("chart"):
            print("there is a chart param")
            portfolio_holdings_by_value = portfolio_holdings_by_value[:100]

        result_page = self.paginator.paginate_queryset(
            portfolio_holdings_by_value, request
        )

        serializer = PortfolioByPeriodSerializer(
            result_page,
            context={"previous_period": previous_period_portfolio_holdings_by_value},
            many=True,
        )

        return_data = self.paginator.get_paginated_response(serializer.data)

        return return_data


@api_view(["GET"])
def portfolio_summary(request, cik, **kwargs):

    cik = Cik.objects.get(cik_number=cik)
    holdings = Holding.objects.filter(
        filing__cik=cik, filing__filing_list=request.period
    )

    summary = holdings.aggregate(
        total_value=Sum("value"),
        total_holdings=Count("cusip", distinct=False),
        unique_cusips=Count("cusip", distinct=True),
    )
    return Response(
        {
            "company_name": cik.filer_name,
            "summary": summary,
        }
    )


@cache_page(60 * 15)
@api_view(["GET"])
def funds_scatterplot(request, **kwargs):
    data = request.period.get_scatterplot_data()
    serializer = FundScatterplotSerializer(data, many=True)
    return Response(serializer.data)


@api_view(["GET"])
def dashboard(request):
    holdings_total = Holding.objects.aggregate(holdings_total=Sum("value")).get(
        "holdings_total"
    )
    filing_count = Filing.objects.all().count()

    average_holding_value = holdings_total / Holding.objects.all().count()

    return Response(
        {
            "holdings_total": holdings_total,
            "filing_count": filing_count,
            "average_holding_value": average_holding_value,
        }
    )
