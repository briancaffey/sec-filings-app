from django.urls import path

from . import views

urlpatterns = [
    path("filing-periods/", views.FilingPeriods.as_view({"get": "get"})),
    path("filings/", views.FilingViewSet.as_view({"get": "get"})),
    path("holdings/", views.HoldingViewSet.as_view({"get": "get"})),
    path(
        "holdings/<str:cik>/",
        views.HoldingViewSet.as_view({"get": "holdings_by_cik"}),
    ),
    path(
        "holdings/<str:cik>/historical/<str:cusip>/",
        views.HoldingViewSet.as_view({"get": "historical_holdings_by_cik"}),
    ),
    path(
        "cik/<str:period>/",
        views.CikViewSet.as_view({"get": "cik_list"}),
        name="cik-list",
    ),
    path(
        "cusip/",
        views.CusipViewSet.as_view({"get": "cusip_list"}),
        name="cusip-list",
    ),
    path(
        "cusip/<str:cusip>/historical/",
        views.CusipViewSet.as_view({"get": "historical_cusip_average_price"}),
        name="historical-cusip",
    ),
    path(
        "cusip/<str:cusip>/<str:period>/",
        views.CusipViewSet.as_view({"get": "get"}),
        name="cusip-detail",
    ),
    path(
        "cusip/<str:cusip>/cik/<str:period>/",
        views.CusipViewSet.as_view({"get": "cik_by_cusip"}),
    ),
    path(
        "cik/<str:cik>/portfolio/historical/",
        views.CikViewSet.as_view({"get": "historical_portfolio_value"}),
    ),
    path(
        "cik/<str:cik>/portfolio/<str:period>/",
        views.CikViewSet.as_view({"get": "portfolio_by_period"}),
        name="portfolio-period",
    ),
    path(
        "cik/<str:cik>/portfolio/summary/<str:period>/",
        views.portfolio_summary,
        name="portfolio-summary",
    ),
    path(
        "funds/scatterplot/<str:period>/",
        views.funds_scatterplot,
        name="fund-scatterplot",
    ),
    path("dashboard/", views.dashboard, name="dashboard"),
]
