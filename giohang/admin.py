from django.contrib import admin
from .models import Gio_Hang,San_Pham_Trong_Gio

# Register your models here.
class giohangadmin(admin.ModelAdmin):
    list_display = ['khach_hang','create_at','update_at']
    
class sanphamgiohangadmin(admin.ModelAdmin):
    list_display = ['gio_hang','san_pham','so_luong']
    
    
admin.site.register(Gio_Hang,giohangadmin)
admin.site.register(San_Pham_Trong_Gio,sanphamgiohangadmin)