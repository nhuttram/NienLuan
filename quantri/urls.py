from django.urls import path, include
from . import views

urlpatterns = [
    path('trangchu/', views.index, name='quantri'),
    path('donhang/', views.quantridonhang , name = 'quantridonhang'),
    path('donhang/huydon/<int:id_huydon>', views.quantrihuydon , name = 'quantrihuydon'),
    path('donhang/chitetidon/<int:id>', views.quantrichitietdon , name = 'quantrichitietdon'),
    
    path('donhang/xoadon/<int:id_huydon>', views.quantrixoadon , name = 'quantrixoadon'),
   
    path('', include('sanpham.urls')),
    # path('', include('khachhang.urls')),

    
]
