from django.urls import path, include
from rest_framework import routers

from .views import CreateOrder, ListOrders, DetailOrder, DeleteOrder, ChangeStatusOrder, AsyncAPIOrder, AsyncSearchAPIOrder

app_name = "orders"

router = routers.DefaultRouter()
router.register(r'', AsyncAPIOrder, basename="api_order")

urlpatterns = [
    path('', ListOrders.as_view(), name="list"),
    path('create/', CreateOrder.as_view(), name="create"),
    path('detail/<int:pk>/', DetailOrder.as_view(), name="detail"),
    path('delete/<int:pk>/', DeleteOrder.as_view(), name="delete"),
    path('change_status/<int:pk>/', ChangeStatusOrder.as_view(), name="change_status"),
    # API
    path("api/v1/", include(router.urls), name="api_order"),
    path("api/v1/search/<str:value_search>", AsyncSearchAPIOrder.as_view(), name="search_order")
]
