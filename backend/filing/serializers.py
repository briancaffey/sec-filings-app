from django.apps import apps

from rest_framework import serializers

from .models import Filing, FilingList, Holding, Cik, Cusip


class FilingPeriodSerializer(serializers.ModelSerializer):
    quarter_name = serializers.SerializerMethodField()

    def get_quarter_name(self, obj):
        year = obj.quarter.year
        month = obj.quarter.month
        if month == 1:
            quarter = "1"
        elif month == 4:
            quarter = "2"
        elif month == 7:
            quarter = "3"
        else:
            quarter = "4"
        return f"Q{quarter} {year}"

    class Meta:
        model = FilingList
        fields = ("id", "quarter", "quarter_name")


class FilingSerializer(serializers.ModelSerializer):
    total_value = serializers.SerializerMethodField()
    cik_number = serializers.SerializerMethodField()
    filer_name = serializers.SerializerMethodField()

    def get_total_value(self, obj):
        return obj.get("total_value")

    def get_cik_number(self, obj):
        return obj.get("cik__cik_number")

    def get_filer_name(self, obj):
        return obj.get("cik__filer_name")

    class Meta:
        model = Filing
        fields = "__all__"
        depth = 2


class CikSerializer(serializers.ModelSerializer):
    current_period_holding_count = serializers.SerializerMethodField()
    total_periods_filed = serializers.SerializerMethodField()
    current_period_fund_size = serializers.SerializerMethodField()

    def get_total_periods_filed(self, obj):
        return obj.get("total_periods_filed")

    def get_current_period_holding_count(self, obj):
        return obj.get("current_period_holding_count")

    def get_current_period_fund_size(self, obj):
        return obj.get("current_period_fund_size")

    class Meta:
        model = Cik
        fields = "__all__"


class HistoricalCusipSerializer(serializers.ModelSerializer):
    class Meta:
        model = FilingList
        fields = ("price_stats", "quarter")

    price_stats = serializers.SerializerMethodField()

    def get_price_stats(self, obj):
        return obj


class CiksByCusipSerializer(CikSerializer):

    total_value = serializers.SerializerMethodField()
    total_shares = serializers.SerializerMethodField()
    first_filed = serializers.SerializerMethodField()
    percent_of_portfolio = serializers.SerializerMethodField()

    def get_first_filed(self, obj):
        return obj.get("first_filed")

    def get_total_value(self, obj):
        return obj.get("total_value")

    def get_total_shares(self, obj):
        return obj.get("total_shares")

    def get_percent_of_portfolio(self, obj):
        return obj.get("percent_of_portfolio")


class HoldingSerializer(serializers.ModelSerializer):
    value = serializers.FloatField()
    sshPrnamt = serializers.FloatField()
    sole = serializers.FloatField()
    shared = serializers.FloatField()
    nonee = serializers.FloatField()

    class Meta:
        model = Holding
        fields = "__all__"
        depth = 3


class HoldingGraphSerializer(serializers.ModelSerializer):
    total = serializers.FloatField(read_only=True)

    class Meta:
        model = Holding
        fields = ("cusip", "nameOfIssuer", "total")


class HoldingHistoricalSerializer(serializers.ModelSerializer):

    cusip_number = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()

    cik_number = serializers.SerializerMethodField()
    filer_name = serializers.SerializerMethodField()

    filing__date_filed = serializers.DateField(format="%m/%d/%Y")
    value = serializers.FloatField()
    sshPrnamt = serializers.FloatField()

    def get_cusip_number(self, obj):
        return obj.get("cusip__cusip_number")

    def get_company_name(self, obj):
        return obj.get("cusip__company_name")

    def get_cik_number(self, obj):
        return obj.get("filing__cik__cik_number")

    def get_filer_name(self, obj):
        return obj.get("filing__cik__filer_name")

    class Meta:
        model = Holding
        fields = (
            "filing__date_filed",
            "sshPrnamt",
            "value",
            "cusip_number",
            "company_name",
            "cik_number",
            "filer_name",
        )


class HistoricalPortfolioValueSerializer(serializers.ModelSerializer):

    value = serializers.FloatField()
    filing_list__quarter = serializers.DateField(format="%m/%d/%Y")

    class Meta:
        model = Filing
        fields = ("filing_list__quarter", "value")


class BaseCusipSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cusip
        fields = "__all__"


class DetailCusipSerializer(BaseCusipSerializer):
    held_by = serializers.SerializerMethodField()
    average_value = serializers.SerializerMethodField()

    def get_held_by(self, obj):
        return self.context.get("held_by")

    def get_average_value(self, obj):
        return self.context.get("average_value")


class CusipSerializer(serializers.ModelSerializer):
    holding_count = serializers.SerializerMethodField()
    held_by_funds = serializers.SerializerMethodField()

    def get_holding_count(self, obj):
        return obj.get("holding_count")

    def get_held_by_funds(self, obj):
        return obj.get("held_by_funds")

    class Meta:
        model = Cusip
        fields = (
            "holding_count",
            "held_by_funds",
            "id",
            "cusip_number",
            "company_name",
        )
        depth = 2


class PortfolioByPeriodSerializer(serializers.ModelSerializer):

    # cusip = serializers.SerializerMethodField()
    total = serializers.FloatField()
    percentage = serializers.FloatField()
    sshPrnamt = serializers.FloatField()
    delta_values = serializers.SerializerMethodField()
    cusip_number = serializers.SerializerMethodField()
    company_name = serializers.SerializerMethodField()

    def get_cusip_number(self, obj):
        return obj.get("cusip__cusip_number")

    def get_company_name(self, obj):
        return obj.get("cusip__company_name")

    def get_delta_values(self, obj):
        cusip = obj.get("cusip")
        current_value = obj.get("total")
        current_shares = obj.get("sshPrnamt")
        current_weight = obj.get("percentage")
        try:
            previous = next(
                (
                    item
                    for item in self.context.get("previous_period")
                    if item["cusip"]["cusip_number"] == cusip.cusip_number
                ),
                None,
            )
            delta_values = {
                "total": (current_value / previous["total"]) - 1,
                "shares": (current_shares / previous["sshPrnamt"]) - 1,
                "weight": (current_weight / previous["percentage"]) - 1,
            }
            return delta_values
        except TypeError:
            delta_values = {"total": None, "shares": None, "weight": None}
            return delta_values

    class Meta:
        model = Holding
        fields = (
            "total",
            # "cusip",
            "cusip_number",
            "company_name",
            "nameOfIssuer",
            "percentage",
            "delta_values",
            "sshPrnamt",
            "sshPrnamtType",
        )


class FundScatterplotSerializer(serializers.ModelSerializer):

    fund_size = serializers.SerializerMethodField()
    holding_count = serializers.SerializerMethodField()
    cik_number = serializers.SerializerMethodField()
    filer_name = serializers.SerializerMethodField()

    def get_fund_size(self, obj):
        return obj.get("fund_size")

    def get_holding_count(self, obj):
        return obj.get("holding_count")

    def get_cik_number(self, obj):
        return obj.get("cik__cik_number")

    def get_filer_name(self, obj):
        return obj.get("cik__filer_name")

    class Meta:
        model = Filing
        fields = ("fund_size", "holding_count", "cik_number", "filer_name")
