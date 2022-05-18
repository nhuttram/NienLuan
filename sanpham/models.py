from django.db import models

from khachhang.models import Khach_Hang

# Create your models here.
class Loai_San_Pham(models.Model):
    loai_ten = models.CharField(default = '',max_length = 255)
    trang_thai = models.BooleanField(default = True)
     
class San_Pham(models.Model):
    ten_san_pham = models.CharField(default = '',max_length = 255)
    loai = models.ForeignKey(Loai_San_Pham, on_delete=models.CASCADE, related_name = 'loai')
    gia = models.IntegerField(default=0)
    so_luong = models.IntegerField(default=0)
    anh_san_pham = models.ImageField(upload_to='anh' ,null = False, default=None)
    mo_ta = models.TextField(default = '')
    trang_thai = models.BooleanField(default=True)
    
    
class Chi_Tiet_San_Pham(models.Model):
    san_pham = models.ForeignKey(San_Pham, on_delete=models.CASCADE, related_name = 'chitietsanpham1',null=True)
    ten = models.CharField(default='',max_length = 255)
    gia_khuyen_mai = models.FloatField(default = 0)
    khuyen_mai = models.IntegerField(default = 0)
    trang_thai = models.BooleanField(default = True)
    
class Binh_Luan(models.Model):
    san_pham = models.ForeignKey(San_Pham, on_delete = models.CASCADE)
    khach_hang = models.ForeignKey(Khach_Hang, on_delete = models.CASCADE)
    noidung = models.CharField(default = '', max_length = 255)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)
    trang_thai = models.BooleanField(default = True)