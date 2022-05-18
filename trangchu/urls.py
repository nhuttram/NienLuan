from django.urls import path, include
from . import views
urlpatterns = [
    path('', views.index  , name="index"),
    path('',  include('khachhang.urls')),
    path('', include('giohang.urls')),
    path('', include('dathang.urls')),
    path('trangchu/sanpham/chitietsanpham/<int:id>/', views.chitietsanpham , name = "chitietsanpham"),
    path('trangchu/sanpham/timkiem/', views.timkiem , name = "timkiem"),
    path('trangchu/sanpham/loaisanpham/<int:id>/', views.loaisanpham , name = "loaisanpham"),
    
    path('trangchu/sanpham/loaisanpham/xoabl/<int:id>/', views.xoabl , name = "xoabinhluan"),
    path('trangchu/email', views.email , name = "email_tudong")
]

handler404="trangchu.views.handle_not_found"