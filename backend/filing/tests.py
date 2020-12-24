import datetime
import os

import pytest
from django.test import override_settings
from django.urls import reverse
from rest_framework.test import APIClient

from .models import FilingList, Filing, Holding
from .factory import (
    FilingFactory,
    FilingListFactory,
    HoldingFactory,
    CikFactory,
    CusipFactory,
)


from .tasks import process_filing, process_filing_file, process_filing_list
from unittest.mock import patch


@pytest.mark.django_db(transaction=True)
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
@patch("filing.utils.download_filing_file")
def test_new_filing_list(save_function):
    """
    This tests that Filings are created
    when a FilingList model is created with a file

    """
    # don't actually download the filings from the filing list
    save_function.side_effect = lambda *args: None
    FilingListFactory(
        quarter=datetime.date(2020, 1, 1),
        filing_year=2020,
        filing_quarter=1,
        datafile__from_path=os.path.join(
            os.getcwd(), "filing", "files", "sample01.txt"
        ),
    )

    filing_list = FilingList.objects.all().first()

    process_filing_list(filing_list.id)

    # the filing list created by the factory
    assert FilingList.objects.count() == 1

    # there are two 13F filings listed in sample01.txt
    assert Filing.objects.count() == 2

    f = FilingList.objects.first()

    filing_1 = Filing.objects.filter(filing_list=f).first()

    # the file should be empty because we patched
    # the download_filing_file method
    assert bool(filing_1.datafile) == False  # noqa

    # clean up file on local file system
    f.datafile.delete()

    # delete the filing list altogether
    f.delete()

    assert FilingList.objects.count() == 0


@pytest.mark.django_db(transaction=True)
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
def test_filing_creation():
    """
    Create a filing list, a filing, Cik and Cusips with Observations
    """
    filing_list = FilingListFactory(
        quarter=datetime.date(2021, 2, 2), filing_quarter=1, filing_year=2020
    )

    # create cik
    cik = CikFactory()

    f = FilingFactory(
        filing_list=filing_list,
        cik=cik,
        datafile__from_path=os.path.join(
            os.getcwd(),
            "filing",
            "files",
            "filings",
            "filing_with_55_holdings.txt",
        ),
    )

    process_filing(f.id)

    assert Holding.objects.all().count() == 55


@pytest.mark.django_db(transaction=True)
@override_settings(CELERY_TASK_ALWAYS_EAGER=True)
def test_process_filing():
    """
    This test the processing of an actual Filing file that is used in a
    FilingFactory instance, we check that it creates the correct number of
    Holding objects
    """
    filing_list = FilingListFactory(quarter=datetime.date(2020, 2, 2))

    cik = CikFactory(cik_number="abc", filer_name="Company A")

    f = FilingFactory(
        datafile__from_path=os.path.join(
            os.getcwd(),
            "filing",
            "files",
            "filings",
            "filing_with_55_holdings.txt",
        ),
        filing_list=filing_list,
        cik=cik,
        date_filed=datetime.date(2020, 3, 3),
    )

    # process the file
    process_filing_file(f.id)

    assert Holding.objects.filter(putCall="CALL").count() == 4
    assert Holding.objects.count() == 55


@pytest.mark.django_db(transaction=True)
def test_get_previous_filing_list():
    filing_q0 = FilingListFactory(
        quarter=datetime.date(2020, 10, 1), filing_year=2020, filing_quarter=4
    )
    filing_q1 = FilingListFactory(
        quarter=datetime.date(2021, 1, 1), filing_year=2021, filing_quarter=1
    )
    filing_q2 = FilingListFactory(
        quarter=datetime.date(2021, 4, 1), filing_year=2021, filing_quarter=2
    )

    q2_previous_filing_list = filing_q2.previous_filing_list()

    assert q2_previous_filing_list.pk == filing_q1.pk
    assert filing_q1.previous_filing_list().pk == filing_q0.pk
    assert filing_q0.previous_filing_list() == None  # noqa


@pytest.mark.skip(reason="Need to rewrite pricing delta logic")
@pytest.mark.django_db(transaction=True)
# @override_settings(DEBUG=False)
def test_previous_filing_deltas():
    filing_q0 = FilingListFactory(
        quarter=datetime.date(2020, 10, 1), filing_year=2020, filing_quarter=4
    )
    filing_q1 = FilingListFactory(
        quarter=datetime.date(2021, 1, 1), filing_year=2021, filing_quarter=1
    )
    filing_q2 = FilingListFactory(
        quarter=datetime.date(2021, 4, 1), filing_year=2021, filing_quarter=2
    )

    # CIK = "A1"
    cik = CikFactory(cik_number="A1", filer_name="Company ABC")
    _filing_0 = FilingFactory(filing_list=filing_q0, cik=cik)  # noqa
    filing_1 = FilingFactory(filing_list=filing_q1, cik=cik)
    filing_2 = FilingFactory(filing_list=filing_q2, cik=cik)

    # holding_0 = HoldingFactory(
    #     filing=filing_0, cusip="abc123", value=100, sshPrnamt=100
    # )

    cusip = CusipFactory(cusip_number="abc123", company_name="Company 1")

    _holding_1 = HoldingFactory(  # noqa
        filing=filing_1, cusip=cusip, value=100, sshPrnamt=100
    )
    _holding_2 = HoldingFactory(  # noqa
        filing=filing_2, cusip=cusip, value=120, sshPrnamt=100
    )

    client = APIClient()
    url = reverse(
        "portfolio-period",
        kwargs={"cik": cik.cik_number, "period": "2021-04-01"},
    )
    resp = client.get(url)
    assert resp.data["results"][0]["percentage"] == 1
    assert float(resp.data["results"][0]["delta_values"]["total"]) == 0.2
    assert resp.status_code == 200


@pytest.mark.django_db(transaction=True)
def test_fund_scatterplot_endpoint():
    filing_q0 = FilingListFactory(
        quarter=datetime.date(2020, 10, 1), filing_year=2020, filing_quarter=4
    )
    # CIK = "A1"
    cik = CikFactory(cik_number="A1", filer_name="Company ABC")
    filing_0 = FilingFactory(filing_list=filing_q0, cik=cik)

    cusip_0 = CusipFactory(cusip_number="abc123", company_name="Company A")
    cusip_1 = CusipFactory(cusip_number="def456", company_name="Company B")

    holding_0_0 = HoldingFactory(  # noqa
        filing=filing_0, cusip=cusip_0, value=100, sshPrnamt=100
    )
    holding_0_1 = HoldingFactory(  # noqa
        filing=filing_0, cusip=cusip_1, value=200, sshPrnamt=200
    )
    client = APIClient()
    url = f"{reverse('fund-scatterplot', kwargs={'period': '2020-10-01'},)}"  # noqa
    resp = client.get(url)

    assert len(resp.data) == 1
    assert resp.data[0]["fund_size"] == 300


@pytest.mark.django_db(transaction=True)
def test_historical_cusip_endpoint():
    """
    Setup 2 filing lists, 1 filing per filing list, and 2 CUSIPs
    that are reported in each filing, then check to see if the values
    from the endpoints are correct
    """
    filing_q0 = FilingListFactory(
        quarter=datetime.date(2020, 10, 1), filing_year=2020, filing_quarter=4
    )
    filing_q1 = FilingListFactory(
        quarter=datetime.date(2021, 1, 1), filing_year=2021, filing_quarter=1
    )

    # CIK = "A1"
    cik_0 = CikFactory(cik_number="A1", filer_name="Company ABC")
    cik_1 = CikFactory(cik_number="B2", filer_name="Company XYZ")
    cik_2 = CikFactory(cik_number="C3", filer_name="Company C3")

    filing_0 = FilingFactory(filing_list=filing_q0, cik=cik_0)
    filing_1 = FilingFactory(filing_list=filing_q1, cik=cik_1)
    filing_2 = FilingFactory(filing_list=filing_q1, cik=cik_2)

    cusip_0 = CusipFactory(cusip_number="abc123", company_name="Security 1")
    cusip_1 = CusipFactory(cusip_number="def456", company_name="Security 2")

    _holding_1 = HoldingFactory(  # noqa
        filing=filing_0, cusip=cusip_0, value=100, sshPrnamt=100
    )
    _holding_2 = HoldingFactory(  # noqa
        filing=filing_1, cusip=cusip_1, value=199, sshPrnamt=100
    )
    _holding_3 = HoldingFactory(  # noqa
        filing=filing_2, cusip=cusip_1, value=201, sshPrnamt=100
    )

    client = APIClient()
    url = f"{reverse('historical-cusip', kwargs={'cusip': 'def456'})}"
    resp = client.get(url)

    assert len(resp.data) == 2
    assert resp.data[0]["price_stats"]["average_value"] == 2000
