from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),

    path('product_gallery/<str:manufacturer>/',
         views.product_gallery, name='product_gallery'),

    path('product_details/<int:smartphone_id>/', views.product_details,
         name='product_details'),

    path('update_basket/<int:item_id>/',
         views.update_basket, name='update_basket'),

    path('remove_from_basket/<int:item_id>/',
         views.remove_from_basket, name='remove_from_basket'),

    path('add_to_basket/', views.add_to_basket, name='add_to_basket'),

    path('basket/', views.basket, name='basket'),

    path('checkout/', views.checkout, name='checkout'),

    path('login/', views.login_user, name='login'),

    path('test/', views.test, name='test'),

    path('register/', views.register_user, name='register'),

    path('apple/', views.apple, name='apple'),

    path('samsung/', views.samsung, name='samsung'),

    path('huawei/', views.huawei, name='huawei'),

    path('xiaomi/', views.xiaomi, name='xiaomi'),

    path('sony/', views.sony, name='sony'),

    path('google/', views.google, name='google'),

]
