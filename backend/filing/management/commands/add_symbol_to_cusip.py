from django.core.management.base import BaseCommand

from filing.tasks import process_fails_to_deliver_data_file


class Command(BaseCommand):
    help = "Add stock tickers to CUSIP data"

    def handle(self, *args, **options):
        years = ["2017", "2018", "2019", "2020"]
        months = [
            "01",
            "02",
            "03",
            "04",
            "05",
            "06",
            "07",
            "08",
            "09",
            "10",
            "11",
            "12",
        ]
        for year in years:
            for month in months:
                for half in ["a", "b"]:
                    URL = f"https://www.sec.gov/files/data/fails-deliver-data/cnsfails{year}{month}{half}.zip"  # noqa
                    process_fails_to_deliver_data_file.delay(URL)
