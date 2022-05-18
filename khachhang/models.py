from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser

import khachhang
# Create your models here.
class Khach_Hang(AbstractUser):
    so_dien_thoai = models.CharField(default='',max_length=15)
    dia_chi = models.CharField(default='', max_length=255)
    
