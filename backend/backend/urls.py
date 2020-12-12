"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path("api/", include("accounts.urls")),
    path("admin/", admin.site.urls),
    path(
        "api/swagger-ui/",
        TemplateView.as_view(
            template_name="swagger-ui.html", extra_context={"schema_url": ""},
        ),
        name="swagger-ui",
    ),
    path("api/", include("core.urls")),
    path("api/", include("filing.urls")),
    path("api/api-auth/", include("rest_framework.urls")),
]

admin.site.site_header = "Open SEC Data Administration"
admin.site.site_title = "Open SEC Data Portal"
admin.site.index_title = "Welcome to the Open SEC Data Admin Portal"


if settings.DEBUG:
    import debug_toolbar  # noqa

    urlpatterns = (
        urlpatterns
        + [path("admin/__debug__/", include(debug_toolbar.urls),)]
        + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
        + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    )
