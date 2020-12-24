import datetime

import factory
from factory.fuzzy import FuzzyChoice, FuzzyDate, FuzzyInteger

from .models import (
    Filing,
    FilingList,
    Holding,
    Cik,
    CikObservation,
    Cusip,
    CusipObservation,
)


class CikFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cik


class CikObservationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CikObservation


class CusipFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Cusip


class CusipObservationFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CusipObservation


class FilingListFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = FilingList

    quarter = FuzzyDate(datetime.date(2015, 1, 1))
    datafile = factory.django.FileField(from_path=None)
    filing_quarter = factory.fuzzy.FuzzyInteger(1, 4)
    filing_year = factory.fuzzy.FuzzyInteger(1993, 2020)


class FilingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Filing

    datafile = factory.django.FileField(from_path=None)
    date_filed = FuzzyDate(datetime.date(2015, 1, 1))
    filing_list = factory.SubFactory(FilingListFactory)
    cik = factory.SubFactory(CikFactory)


class HoldingFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Holding

    filing = factory.SubFactory(FilingFactory)
    nameOfIssuer = factory.Faker("company")
    titleOfClass = factory.Faker("bs")
    cusip = factory.SubFactory(CusipFactory)
    value = FuzzyInteger(0, 1000)
    sshPrnamt = FuzzyInteger(0, 1000)
    sshPrnamtType = FuzzyChoice(["SH"])
    # investmentDiscretion =
    # putCall =
    # otherManager =
    sole = FuzzyInteger(0, 1000)
    shared = FuzzyInteger(0, 1000)
    nonee = FuzzyInteger(0, 1000)
