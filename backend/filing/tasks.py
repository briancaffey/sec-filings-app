import datetime
import io
import logging
import urllib.request
import zipfile


from collections import namedtuple

from backend.celery_app import app

from django.apps import apps

from .utils import (
    process_filing_file,
    save_filing_file_to_model,
    save_filing_list_file_to_model,
)

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)


@app.task(queue="default")
def process_filing_list(filing_list_id):

    FilingList = apps.get_model("filing", "FilingList")
    Filing = apps.get_model("filing", "Filing")

    Cik = apps.get_model("filing", "Cik")
    CikObservation = apps.get_model("filing", "CikObservation")

    filing_list = FilingList.objects.get(pk=filing_list_id)

    if not filing_list.datafile:
        logger.info("no filing list datafile, downloading file from SEC")
        save_filing_list_file_to_model(filing_list.id)

    logger.info("####  Processing File  ####")
    lines = filing_list.datafile.read().decode("utf-8").split("\n")

    FilingTuple = namedtuple(
        "Filing",
        ["cik", "company_name", "form_type", "date_filed", "filename"],
    )

    # build list of 13F filing data
    filings_13f = []
    for line in lines:
        if ".txt" in line:
            data = line.split("|")
            filing = FilingTuple(*data)
            if "13F-HR" in filing.form_type:
                filings_13f.append(filing)

    filing_records_to_create = []
    for filing in filings_13f:

        # get_or_create_cik
        cik, _ = Cik.objects.get_or_create(cik_number=filing.cik)

        if not cik.filer_name:
            cik.filer_name = filing.company_name

        cik.save()

        cik_observation = CikObservation(
            name=filing.company_name, filing_list=filing_list, cik=cik
        )

        cik_observation.save()

        filing_record = Filing(
            cik=cik,  # this uses the model created above
            form_type=filing.form_type,
            date_filed=datetime.datetime.strptime(
                filing.date_filed, "%Y-%m-%d"
            ),
            filename=filing.filename,
            filing_list=filing_list,
        )

        filing_records_to_create.append(filing_record)
    Filing.objects.bulk_create(filing_records_to_create)

    for filing in Filing.objects.filter(filing_list=filing_list):
        process_filing.delay(filing.id)

    return f"Finished processing Filing {filing_list_id}"


@app.task(queue="default")
def process_filing(filing_id):
    """
    Process a filing

    The actual file will not exist, so we will need to
    download it before processing

    this function:

    - downloads the file, bulk creates holdings
    """
    logger.info(f"processing filing {filing_id}")
    Filing = apps.get_model("filing", "Filing")
    filing = Filing.objects.get(pk=filing_id)

    logger.info(f"deleting holdings for filing {filing_id}")
    filing.delete_holdings()

    # download the data for the filing
    logger.info("checking presence of datafile")
    if not filing.datafile:
        logger.info("no datafile, downloading file from SEC")
        save_filing_file_to_model(filing_id)

    # once it has been downloaded, process the file
    logger.info(f"processing downloaded filing file {filing_id}")
    process_filing_file(filing.id)
    logger.info(f"finished processing filing {filing_id}")
    return f"Finished processing filing {filing_id}."


# https://stackoverflow.com/questions/94490/how-do-i-read-selected-files-from-a-remote-zip-archive-over-http-using-python
@app.task
def process_fails_to_deliver_data_file(url):
    Cusip = apps.get_model("filing", "Cusip")
    try:
        remotezip = urllib.request.urlopen(url)
        zipinmemory = io.BytesIO(remotezip.read())
        zip = zipfile.ZipFile(zipinmemory)
        for fn in zip.namelist():
            if fn.endswith(".txt"):
                file_data = zip.read(fn)
                for line in file_data.decode("utf-8").split("\n")[1:]:
                    data = line.split("|")
                    if True:
                        cusip_number = data[1]
                        symbol = data[2]
                        cusip = Cusip.objects.filter(
                            cusip_number=cusip_number
                        ).first()
                        if cusip:
                            cusip.symbol = symbol
                            cusip.save()

                    # do something with each line
    except urllib.request.HTTPError:
        pass
