from django.urls import path, include

urlpatterns = [
    path("", include("cinex360.urls")),
    path("", include("portfolio.urls")),
    path("", include("siddhitaarts.urls")),
]
