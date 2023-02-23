from django.urls import path

from .views import SummaryApiView

urlpatterns = [
    path('', SummaryApiView.as_view())
]
