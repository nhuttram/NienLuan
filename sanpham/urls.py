from django.urls import path
from . import views


urlpatterns = [
    # lấy ra các loại hành
    path('quantri/loaihang/', views.get_loai , name = 'loaihang'),
    # them loai hang
    path('loaihangreturn', views.add_loai),
    path('themloaihang/', views.get_loaihangform),
    # xoa loai hang
    path('xoaloai/<int:id>/', views.xoa_loai , name = 'xoa_loai'),
    # sửa loại hàng
    path('sualoai/<int:id>/', views.sua_loai , name ='sua_loai'),
    
    # san pham
    path('quantri/sanpham.html', views.get_sanpham, name = 'sanpham'),
      # hien thi form
    path('quantri/sanpham/themsanpham.html', views.get_sanphamform, name = 'them_san_pham'),  
    # them san pham
    path('sanphamreturn', views.add_sanpham),
     # xoa san pham
    path('xoasanpham/<int:id>/', views.xoa_san_pham , name = 'xoa_san_pham'),
    # sửa loại hàng
    path('quantri/sanpham/suasanpham/<int:id>/', views.sua_san_pham , name ='sua_san_pham'),
    #  xuất file
    path('xuatfilesp', views.xuatfilesp , name='xuatfilesp'),
    # giảm giá 
    path('quantri/giamgia/', views.giamgia, name = 'giamgia'),
    
    path('quantri/sanpham/giamgia/<int:id>/', views.giam_gia_san_pham , name ='giam_gia_san_pham'),
    path('xoagiamgia/<int:id>/', views.xoa_giam_gia , name ='xoa_giam_gia'),
    
]

