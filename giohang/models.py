from unicodedata import decimal
from django.db import models

from khachhang.models import Khach_Hang
from sanpham.models import San_Pham

# Create your models here.
class Gio_Hang(models.Model):
    khach_hang = models.ForeignKey(Khach_Hang, on_delete=models.CASCADE )
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    
class San_Pham_Trong_Gio(models.Model):
    gio_hang = models.ForeignKey(Gio_Hang, on_delete=models.CASCADE, related_name = 'gio_hang')
    san_pham = models.ForeignKey(San_Pham, on_delete=models.CASCADE, related_name = 'san_pham_gio')
    so_luong = models.IntegerField(default=0)
