from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop, name='shop'),

    path('product_gallery/', views.product_gallery, name='product_gallery'),

    path('product_details/', views.product_details, name='product_details'),

    path('basket/', views.basket, name='basket'),

    path('checkout/', views.checkout, name='checkout'),

    path('login/', views.login_user, name='login'),

    path('logout/', views.logout_user, name='logout'),

    path('test/', views.test, name='test'),

    path('register/', views.register_user, name='register'),

    path('apple/', views.apple, name='apple'),

    path('samsung/', views.samsung, name='samsung'),

    path('huawei/', views.huawei, name='huawei'),

    path('xiaomi/', views.xiaomi, name='xiaomi'),

    path('sony/', views.sony, name='sony'),

    path('google/', views.google, name='google'),

    path('shopBackend/', views.shopBackend, name='shopBackend'),

]
