from django.urls import path
from django.views.generic import TemplateView

from .views import OpenShift, CloseShift, ShiftList, ShiftDetail

app_name = "shift"


urlpatterns = [
    path("/", ShiftList.as_view(), name="list"),
    path("open_shift/", OpenShift.as_view(), name="open"),
    path("close_shift/", CloseShift.as_view(), name="close"),
    path("shift_exist/", TemplateView.as_view(template_name="shift/exist_shift.html"), name="exist"),
    path("detail_shift/<int:pk>/", ShiftDetail.as_view(), name="detail"),
]
