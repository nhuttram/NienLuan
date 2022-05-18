from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views
urlpatterns = [
    #quan tri khach hàng
    path('quantri/quantrikhachhang/', views.viewkhachhang ,name = "quantrikhachhang" ),
    #quan tri xoa khach hang
    path('quantri/quantrikhachhang/xoakhachhang/<int:id>/', views.xoakhachhang , name = "quantrixoakhachhang" )
    ,
    # đăng nhập và đăng xuất
    path('trangchu/dangnhap/', auth_views.LoginView.as_view(template_name="pages/dangnhap.html"), name="dangnhap"),
    path('trangchu/dangxuat/', auth_views.LogoutView.as_view(next_page= '/'), name="dangxuat"),
    #  đăng ký tài khoảng
    path('trangchu/dangky/', views.dangky, name="dangki"),
    # doi mat khau 
    path('trangchu/doimatkhau.html', views.doimatkhau, name="doimatkhau"),
    # thong tin ca nhan
    path('trangchu/thongtinkhachhang.html', views.thongtinkhachhang, name="thongtinkhachhang"),
    
  
]