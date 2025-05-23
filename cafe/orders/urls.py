from django.urls import path, include
from rest_framework import routers
from django.views.generic import TemplateView

from .views import CreateOrder, ListOrders, DetailOrder, DeleteOrder, ChangeStatusOrder, APIOrder, SearchAPIOrder

app_name = "orders"

router = routers.DefaultRouter()
router.register(r'', APIOrder, basename="api_order")

urlpatterns = [
    path('', ListOrders.as_view(), name="list"),
    path("shift_exist/", TemplateView.as_view(template_name="shift/exist_shift.html"), name="exist_shift"),
    path('create/', CreateOrder.as_view(), name="create"),
    path("search/", SearchAPIOrder.as_view(), name="search_order"),
    path('detail/<int:pk>/', DetailOrder.as_view(), name="detail"),
    path('delete/<int:pk>/', DeleteOrder.as_view(), name="delete"),
    path('change_status/<int:pk>/', ChangeStatusOrder.as_view(), name="change_status"),
    # API
    path("api/v1/", include(router.urls), name="api_order"),
]
