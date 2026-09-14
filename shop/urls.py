from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.product_list, name='product_list'),
    path('products/<int:pk>/', views.product_detail, name='product_detail'),

    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/<int:pk>/', views.cart_add, name='cart_add'),
    path('cart/increase/<int:pk>/', views.cart_increase, name='cart_increase'),
    path('cart/decrease/<int:pk>/', views.cart_decrease, name='cart_decrease'),
    path('cart/remove/<int:pk>/', views.cart_remove, name='cart_remove'),
    path('cart/set/<int:pk>/', views.cart_set_quantity, name='cart_set_quantity'),

    path('checkout/', views.checkout, name='checkout'),
    path('order-success/', views.order_success, name='order_success'),
]
