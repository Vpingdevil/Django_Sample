from django.contrib import admin
from django.urls import path, include
from django.contrib.sitemaps.views import sitemap
from medicines.sitemaps import MedSiteMap
from django.views.generic import TemplateView


sitemaps = {
    'medicines': MedSiteMap
}

urlpatterns = [
    path("robots.txt", TemplateView.as_view(template_name="robots.txt", content_type="text/plain"), name="robots"),
    path("sitemap.xml/", sitemap, {'sitemaps': sitemaps}, name="sitemap"),
    path("", include("home.urls")),
    path("", include("cart.urls")),
    path('admin/', admin.site.urls),
    path('medicines/', include("medicines.urls")),
    path("", include("checkout.urls")),
    # path("", include("django.contrib.auth.urls")),  # Builtins
    path("", include("accounts.urls")),
    path("", include("allauth.urls")),
    path("api/v1/", include("api.urls")),
]
