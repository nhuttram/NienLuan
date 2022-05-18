import datetime
from django.db import models
# Create your models here.
from giohang.models import Gio_Hang
from khachhang.models import Khach_Hang
from sanpham.models import San_Pham
# Create your models here.
class Dat_Hang(models.Model):
    khach_hang = models.ForeignKey(Khach_Hang, on_delete=models.CASCADE)
   # gio_hang = models.ForeignKey(Gio_Hang, on_delete= models.CASCADE, related_name = 'dathang_giohang')
    hinh_thuc = models.CharField(max_length = 255, default = 'truc_tiep')
    trang_thai_dat_hang = models.CharField(max_length = 255, default = 'chua_xac_nhan')
    tongtien = models.FloatField(default = 0)
    trang_thai = models.IntegerField(default=0) #trang thái = 1 đơn hàng đã được thanh toán, = 0 đơn hàng chauw dx thanh toán
    create_at = models.DateTimeField(auto_now_add=True, null=True)
    update_at = models.DateTimeField(auto_now=True, null=True)
    
    
class Chi_Tiet_Dat_Hang(models.Model):
    dat_hang = models.ForeignKey(Dat_Hang, on_delete=models.CASCADE ,related_name = 'dat_hang' )
    san_pham = models.ForeignKey(San_Pham, on_delete=models.CASCADE)
    so_luong = models.IntegerField(default=0)
    giam_gia = models.IntegerField(default=0, null=True)
    