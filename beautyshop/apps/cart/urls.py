from django.urls import path

from . import views

urlpatterns = [
    path('', views.cart_detail, name='cart'),
    path('orderForm/', views.orderForm, name='orderForm'),
    path('success/', views.success, name='success')
]