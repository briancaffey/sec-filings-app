import datetime
from django.core.management.base import BaseCommand

from filing.models import FilingList


class Command(BaseCommand):
    help = "Generates all filing lists from 1993 to present, but doesn't download files"

    def handle(self, *args, **options):
        month_mapping = {1: 1, 2: 4, 3: 7, 4: 10}
        for year in range(1993, 2021):
            for quarter in range(1, 5):
                month = month_mapping[quarter]
                filing_list, created = FilingList.objects.get_or_create(
                    filing_year=year,
                    filing_quarter=quarter,
                    quarter=datetime.date(year, month, 1),
                )
