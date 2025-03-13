from django.urls import path

from .views import CreateOrder, ListOrders, DetailOrder, DeleteOrder, ChangeStatusOrder

app_name = "orders"

urlpatterns = [
    path('', ListOrders.as_view(), name="list"),
    path('create/', CreateOrder.as_view(), name="create"),
    path('detail/<int:pk>/', DetailOrder.as_view(), name="detail"),
    path('delete/<int:pk>/', DeleteOrder.as_view(), name="delete"),
    path('change_status/<int:pk>/', ChangeStatusOrder.as_view(), name="change_status"),
]
