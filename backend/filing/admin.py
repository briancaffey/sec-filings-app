from django.contrib import admin
from django.core.management import call_command
from django.utils.html import format_html
from django.db import models
from django.http import HttpResponseRedirect

from django.urls import path

# Register your models here.

from .models import (
    FilingList,
    Filing,
    Holding,
    Cik,
    Cusip,
    CikObservation,
    CusipObservation,
)

from .tasks import process_filing, process_filing_list


class CikAdmin(admin.ModelAdmin):
    class Meta:
        model = Cik

    search_fields = ("cik_number",)
    list_display = ("cik_number", "filer_name")


class CusipAdmin(admin.ModelAdmin):
    class Meta:
        model = Cusip

    search_fields = ("cusip_number", "company_name", "symbol")
    list_display = ("cusip_number", "company_name", "symbol")


class CikObservationAdmin(admin.ModelAdmin):
    class Meta:
        model = CikObservation

    search_fields = ("cik__cik_number", "name")
    readonly_fields = ("cik", "filing_list", "name")
    list_display = ("id", "cik", "name", "filing_list")


class CusipObservationAdmin(admin.ModelAdmin):
    class Meta:
        model = CusipObservation

    search_fields = ("cusip__cusip_number", "name")
    # raw_id_fields = ["cusip", "name"]
    readonly_fields = ("cusip", "name", "filing")
    list_display = ("id", "cusip", "name", "filing")


class FilingListAdmin(admin.ModelAdmin):
    class Meta:
        model = FilingList

    list_display = ("id", "datafile", "quarter", "filing_count")

    change_form_template = "admin/filing/filinglist/change_form.html"

    def process_filings(self, request, queryset):
        for filing_list in queryset:
            filing_list.process_filing_list()

    actions = [process_filings]

    process_filings.short_description = "Process Filings"

    def get_urls(self):
        urls = super().get_urls()
        filing_list_urls = [path("generate/", self.generate_filing_lists)]
        return urls + filing_list_urls

    def generate_filing_lists(self, request):

        call_command("generate_filing_lists")
        self.message_user(request, "Filing lists have been generated (1993 - 2020).")

        return HttpResponseRedirect("../")

    def response_change(self, request, obj):
        if "_process_filing_list" in request.POST:
            process_filing_list.apply_async(args=(obj.id,))
            self.message_user(request, "Filing list is being processed.")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


class FilingAdmin(admin.ModelAdmin):
    class Meta:
        model = Filing

    # https://stackoverflow.com/questions/46756086/django-admin-edit-model-select-prefetch-related
    list_select_related = ("filing_list",)
    readonly_fields = ("filing_list",)

    list_display = (
        "id",
        "cik",
        "form_type",
        "date_filed",
        "filing_list_link",
        "datafile",
        "holding_count",
    )

    search_fields = ("form_type",)

    # def holding_count(self, obj=None):
    #     return obj.holding_count()

    def holding_count(self, obj=None):
        return format_html(
            f"<a href='/admin/filing/holding/?filing__id={obj.id}'>{obj.holding_count()}</a>"
        )

    holding_count.admin_order_field = "holdingcount"

    def filing_list_link(self, obj=None):
        return format_html(
            f'<a target="_blank" href="/admin/filing/filinglist/{obj.filing_list.id}/change/">{str(obj.filing_list)}</a>'
        )

    change_form_template = "admin/filing/filing/change_form.html"

    def response_change(self, request, obj):
        if "_process_filing" in request.POST:
            process_filing.apply_async(args=(obj.id,))
            self.message_user(request, "Filing is being processed.")
            return HttpResponseRedirect(".")
        return super().response_change(request, obj)


class HoldingAdmin(admin.ModelAdmin):
    class Meta:
        model = Holding

    # raw_id_fields = ["filing"]

    list_select_related = ("filing",)

    readonly_fields = ("filing",)
    list_display = (
        "id",
        "cik",
        "filing_link",
        "filing",
        "date_filed",
        "nameOfIssuer",
        "titleOfClass",
        "cusip",
        "value",
        "sshPrnamt",
        "sshPrnamtType",
        "investmentDiscretion",
        "putCall",
        "otherManager",
        "sole",
        "shared",
        "nonee",
    )

    def cik(self, obj=None):
        return format_html(
            f'<a target="_blank" href="/cik/{obj.filing.cik}">{obj.filing.cik}</a>'
        )

    def date_filed(self, obj=None):
        return obj.filing.date_filed

    # https://stackoverflow.com/questions/2168475/django-admin-how-to-sort-by-one-of-the-custom-list-display-fields-that-has-no-d
    date_filed.admin_order_field = "filing__date_filed"

    def filing_link(self, obj=None):
        return format_html(
            f'<a target="_blank" href="/admin/filing/filing/{obj.filing.id}/change/">Link</a>'
        )

    search_fields = ("nameOfIssuer", "cusip__cusip_number", "cusip__company_name")


admin.site.register(Holding, HoldingAdmin)
admin.site.register(FilingList, FilingListAdmin)
admin.site.register(Filing, FilingAdmin)
admin.site.register(Cik, CikAdmin)
admin.site.register(CikObservation, CikObservationAdmin)
admin.site.register(Cusip, CusipAdmin)
admin.site.register(CusipObservation, CusipObservationAdmin)
