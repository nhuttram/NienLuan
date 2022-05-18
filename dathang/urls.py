from django.urls import path
from . import views

urlpatterns = [
    path('trangchu/gio_hang/<int:id>/dathang.html', views.dat_hang, name = 'dat_hang'),
    path('post/ajax', views.thanh_toan_pay_pal, name = 'thanh_toan'),
    path('trangchu/thanh_toan_truc_tiep/<int:id>/', views.thanh_toan_truc_tiep, name = 'thanh_toan_truc_tiep'),
    
    # don hang
    path('trangchu/khachhang/donhang.html', views.donhang, name="donhang"),
    
    #chi tiet don
    path('trangchu/khachhang/donhangchitiet/<int:id>', views.chitiet_donhang, name="chitiet_donhang"),
 
    
    # huy don
    path('<int:id_huydon>', views.huydon, name="huydon"),
]