from collections import namedtuple
import io
import re
import logging
import urllib.request
import xml.etree.ElementTree as ET

from django.apps import apps
from django.core.files.base import ContentFile

logger = logging.getLogger("django")
logger.setLevel(logging.INFO)

BASE_URL = "https://www.sec.gov/Archives/"
XML_SCHEMA = "{http://www.sec.gov/edgar/document/thirteenf/informationtable}"


def process_filing_file(filing_id):

    Cusip = apps.get_model("filing", "Cusip")

    Filing = apps.get_model("filing", "Filing")
    Holding = apps.get_model("filing", "Holding")

    Cusip = apps.get_model("filing", "Cusip")
    CusipObservation = apps.get_model("filing", "CusipObservation")

    filing = Filing.objects.get(pk=filing_id)
    xml_data = filing.datafile.read().decode("utf-8")

    # python's xml module can't parse the SEC filing's format,
    # so we use regex to pull out the two XML sections for
    # edgar_submission and information_table
    matches = re.findall(r"<XML>[\s\S]*?<\/XML>", xml_data)
    xml_entities = [x[5:-6].replace("\n", "") for x in matches]
    assert len(xml_entities) == 2

    edgar_submission = ET.fromstring(xml_entities[0])  # noqa
    information_table = ET.fromstring(xml_entities[1])

    HoldingTuple = namedtuple(
        "Holding",
        [
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
        ],
    )

    holding_tuples = []
    for _, infoTable in enumerate(
        information_table.findall(f"{XML_SCHEMA}infoTable")
    ):
        nameOfIssuer = infoTable.find(f"{XML_SCHEMA}nameOfIssuer").text
        titleOfClass = infoTable.find(f"{XML_SCHEMA}titleOfClass").text
        cusip = infoTable.find(f"{XML_SCHEMA}cusip").text.upper()
        value = infoTable.find(f"{XML_SCHEMA}value").text
        sshPrnamt = infoTable.find(
            f"{XML_SCHEMA}shrsOrPrnAmt/{XML_SCHEMA}sshPrnamt"
        ).text
        sshPrnamtType = infoTable.find(
            f"{XML_SCHEMA}shrsOrPrnAmt/{XML_SCHEMA}sshPrnamtType"
        ).text
        putCall = infoTable.find(f"{XML_SCHEMA}putCall")
        # putCall is not always present
        if putCall is not None:
            putCall = putCall.text.upper()
        else:
            putCall = None
        otherManager = infoTable.find(f"{XML_SCHEMA}otherManager")
        # otherManager is not always present
        if otherManager is not None:
            otherManager = otherManager.text
        else:
            otherManager = None
        investmentDiscretion = infoTable.find(
            f"{XML_SCHEMA}investmentDiscretion"
        ).text
        Sole = infoTable.find(
            f"{XML_SCHEMA}votingAuthority/{XML_SCHEMA}Sole"
        ).text
        Shared = infoTable.find(
            f"{XML_SCHEMA}votingAuthority/{XML_SCHEMA}Shared"
        ).text
        None_ = infoTable.find(
            f"{XML_SCHEMA}votingAuthority/{XML_SCHEMA}None"
        ).text

        data = {
            "nameOfIssuer": nameOfIssuer,
            "titleOfClass": titleOfClass,
            "cusip": cusip,
            "value": value,
            "sshPrnamt": sshPrnamt,
            "sshPrnamtType": sshPrnamtType,
            "otherManager": otherManager,
            "investmentDiscretion": investmentDiscretion,
            "putCall": putCall,
            "sole": Sole,
            "shared": Shared,
            "nonee": None_,
        }

        holding_tuples.append(HoldingTuple(**data))
        # holdings.append(data)
    # logger.info(holdings)

    # do a bulk create on holding data, remember to pass in filing id
    holding_records_to_create = []
    for holding in holding_tuples:

        # get_or_create_cusip

        cusip, _ = Cusip.objects.get_or_create(cusip_number=holding.cusip)

        if not cusip.company_name:
            cusip.company_name = holding.nameOfIssuer

        cusip.save()

        cusip_observation = CusipObservation(
            name=holding.nameOfIssuer, filing=filing, cusip=cusip
        )

        cusip_observation.save()

        # check holdings, run checks, potentially flag holdings
        holding_record = Holding(
            # add Holding fields
            nameOfIssuer=holding.nameOfIssuer,
            titleOfClass=holding.titleOfClass,
            cusip=cusip,
            value=holding.value,
            sshPrnamt=holding.sshPrnamt,
            sshPrnamtType=holding.sshPrnamtType,
            investmentDiscretion=holding.investmentDiscretion,
            putCall=holding.putCall,
            otherManager=holding.otherManager,
            sole=holding.sole,
            shared=holding.shared,
            nonee=holding.nonee,
            filing=filing,
        )

        holding_records_to_create.append(holding_record)

    Holding.objects.bulk_create(holding_records_to_create)


def download_filing_list_file(filing_list_id):

    FilingList = apps.get_model("filing", "FilingList")
    filing_list = FilingList.objects.get(pk=filing_list_id)
    BASE_URL = "https://www.sec.gov/Archives/edgar/full-index"
    # https://www.sec.gov/Archives/edgar/full-index/2021/QTR1/
    filing_list_url = f"{BASE_URL}/{filing_list.filing_year}/QTR{filing_list.filing_quarter}/master.idx"  # noqa

    logger.info(filing_list_url)
    req = urllib.request.Request(
        filing_list_url,
        data=None,
        headers={
            'User-Agent': 'Open SEC Data brian@opensecdata.ga',
            'Host': 'www.sec.gov'
        }
    )
    response = urllib.request.urlopen(req)

    data = response.read()
    return io.BytesIO(data)


def save_filing_list_file_to_model(filing_list_id):

    FilingList = apps.get_model("filing", "FilingList")
    filing_list = FilingList.objects.get(pk=filing_list_id)
    with download_filing_list_file(filing_list_id) as fh:
        filing_list.datafile = ContentFile(fh.getvalue())
        filing_list.datafile.name = f"filing-list-{filing_list.filing_year}-{filing_list.filing_quarter}.txt"  # noqa
        filing_list.save()


def download_filing_file(filing_id):
    Filing = apps.get_model("filing", "Filing")
    filing = Filing.objects.get(pk=filing_id)
    filing_url = f"{BASE_URL}{filing.filename}"
    req = urllib.request.Request(
        filing_url,
        data=None,
        headers={
            'User-Agent': 'Open SEC Data brian@opensecdata.ga',
            'Host': 'www.sec.gov'
        }
    )
    response = urllib.request.urlopen(req)
    data = response.read()
    return io.BytesIO(data)


def save_filing_file_to_model(filing_id):
    Filing = apps.get_model("filing", "Filing")
    filing = Filing.objects.get(pk=filing_id)
    with download_filing_file(filing_id) as fh:
        filing.datafile = ContentFile(fh.getvalue())
        filing.datafile.name = filing.filename
        filing.save()
