import logging

from django.apps import apps
from django.db import models
from django.db.models.signals import post_save

from .tasks import process_filing_list

# Create your models here.

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


class FilingListManager(models.Manager):
    def get_queryset(self):
        return (
            super(FilingListManager, self)
            .get_queryset()
            .annotate(filingcount=models.Count("filinglist"))
        )


class CikObservation(models.Model):
    name = models.CharField(max_length=1000, blank=False, null=False)
    filing_list = models.ForeignKey(
        "FilingList", related_name="filing_list_observation", on_delete=models.CASCADE
    )

    cik = models.ForeignKey(
        "Cik", related_name="observation_for_cik", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.name} CikObservation"


class Cik(models.Model):
    cik_number = models.CharField(max_length=100, blank=False, null=False)
    filer_name = models.CharField(max_length=1000, blank=False, null=False)
    # alternate_filer_names = models.ManyToManyField(CikObservation)

    def __str__(self):
        return f"{self.cik_number} (CIK)"


class CusipObservation(models.Model):
    name = models.CharField(max_length=100, blank=False, null=False)
    filing = models.ForeignKey(
        "Filing", related_name="filing_observation", on_delete=models.CASCADE
    )
    cusip = models.ForeignKey(
        "Cusip", related_name="cusip_for_observation", on_delete=models.CASCADE
    )


class Cusip(models.Model):
    cusip_number = models.CharField(max_length=100, blank=False, null=False)
    company_name = models.CharField(max_length=1000, blank=False, null=False)
    symbol = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return f"{self.cusip_number} (CUSIP)"


class FilingList(models.Model):
    """
    A quarterly file that contains all SEC listings
    About 6000 filings of the 250,000 filings in this index file are 13F filings
    Example filing index: https://www.sec.gov/Archives/edgar/full-index/2020/QTR1/master.idx
    All filing indexes: https://www.sec.gov/Archives/edgar/full-index/
    """

    objects = FilingListManager()

    datafile = models.FileField(null=True, blank=True)

    quarter = models.DateField()

    filing_quarter = models.IntegerField(null=False, blank=False)

    filing_year = models.IntegerField(null=False, blank=False)

    def __str__(self):
        return f"Filing List ({self.quarter})"

    def process_filing_list(self):
        logger.info(f"Sending 'Process Filing List' task to celery for {self}.")
        process_filing_list.delay(self.id)

    def filing_count(self):
        return self.filingcount

    def previous_filing_list(self):
        return (
            FilingList.objects.filter(quarter__lt=self.quarter)
            .order_by("-quarter")
            .first()
        )

    filing_count.admin_order_field = "filingcount"

    class Meta:
        ordering = ("-quarter",)

    def get_scatterplot_data(self):
        Filing = apps.get_model("filing", "Filing")
        return (
            Filing.objects.filter(filing_list=self)
            .prefetch_related("cik")
            .annotate(
                holding_count=models.Count("filing"),
                fund_size=models.Sum("filing__value"),
            )
            # .filter(fund_size__lte=100_000_000)
            # .filter(holding_count__lte=5000)
            .values("fund_size", "holding_count", "cik__cik_number", "cik__filer_name")
            .order_by("-holding_count")
        )


class FilingManager(models.Manager):
    def get_queryset(self):
        return (
            super(FilingManager, self)
            .get_queryset()
            .annotate(holdingcount=models.Count("filing"))
        )


class Filing(models.Model):

    """
    A 13F filing from EDGAR
    e.g.: https://www.sec.gov/Archives/edgar/data/1000097/0001000097-20-000004.txt
    """

    objects = FilingManager()

    # cik = models.CharField(max_length=100, blank=False, null=False)
    cik = models.ForeignKey("Cik", related_name="filing_cik", on_delete=models.CASCADE)

    form_type = models.CharField(max_length=100, blank=False, null=False)

    date_filed = models.DateField()

    filename = models.CharField(max_length=300, blank=False, null=False)

    datafile = models.FileField()

    filing_list = models.ForeignKey(
        "FilingList", related_name="filinglist", on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.cik.filer_name} (Q{self.filing_list.filing_quarter}-{self.filing_list.filing_year})"

    def delete_holdings(self):
        Holding.objects.filter(filing=self).delete()

    def holding_count(self):
        return self.holdingcount

    holding_count.admin_order_field = "holdingcount"


class Holding(models.Model):
    """
    The holding data for a postition in a 13F filing
    """

    filing = models.ForeignKey(
        "Filing", related_name="filing", on_delete=models.CASCADE
    )
    nameOfIssuer = models.CharField(max_length=500, blank=True, null=True)
    titleOfClass = models.CharField(max_length=500, blank=True, null=True)
    # cusip_raw = models.CharField(max_length=500, blank=True, null=True)
    cusip = models.ForeignKey("Cusip", related_name="cusip", on_delete=models.CASCADE)
    value = models.DecimalField(
        "value",
        null=True,
        blank=True,
        max_digits=19,
        decimal_places=2,
    )
    sshPrnamt = models.DecimalField(
        "sshPrnamt",
        null=True,
        blank=True,
        max_digits=19,
        decimal_places=2,
    )
    sshPrnamtType = models.CharField(max_length=500, blank=True, null=True)
    investmentDiscretion = models.CharField(max_length=500, blank=True, null=True)
    putCall = models.CharField(max_length=500, blank=True, null=True)
    otherManager = models.CharField(max_length=500, blank=True, null=True)
    sole = models.DecimalField(
        "sole",
        null=True,
        blank=True,
        max_digits=19,
        decimal_places=2,
    )
    shared = models.DecimalField(
        "shared",
        null=True,
        blank=True,
        max_digits=19,
        decimal_places=2,
    )
    nonee = models.DecimalField(
        "nonee",
        null=True,
        blank=True,
        max_digits=19,
        decimal_places=2,
    )

    class Meta:
        # ordering = ('nameOfIssuer', 'id')
        ordering = ("filing__date_filed", "id")
