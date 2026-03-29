from django.urls import path

from . import views

app_name = "orders"

urlpatterns = [
    path("", views.my_orders, name="my_orders"),
    path("checkout/", views.checkout, name="checkout"),
    path("place/", views.place_order, name="place"),
    path("<int:order_id>/", views.order_detail, name="detail"),
]