from django.urls import path
from . import views

app_name = 'cart'
urlpatterns = [
    path('detail', views.CartDetailView.as_view(), name='cart_detail'),
    path('add/<slug:slug>',views.AddToCartView.as_view(), name='cart_add'),
    path('delete/<str:id>',views.DeleteCartView.as_view(), name='cart_delete'),
    path('order/detail/<int:pk>',views.OrderDetailView.as_view(), name='order_detail'),
    path('order/add',views.AddOrderView.as_view(), name='order_add'),
    path('apply/discount/code/<int:pk>',views.ApplyDiscountView.as_view(), name='apply_discount'),
    path("request/<int:pk>/", views.SendRequestView.as_view(), name="send_request"),
    path("verify/", views.CartVerifyView.as_view(), name="request_verify"),
]