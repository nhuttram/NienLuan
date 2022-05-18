from django.urls import path,include
from . import views

urlpatterns = [
    path('trangchu/giohang/<int:id_giohang>', views.giohang , name = "giohang"),
    path('trangchu/giohang/', views.giohang),
    path('trangchu/themvaogiohang/<int:id>', views.themgiohang , name = "muasanpham"),
    path('trangchu/giohang/xoa/<int:idgio>&<int:san_pham>', views.xoagio , name = "xoagio"),
   
  
    
]
    
 