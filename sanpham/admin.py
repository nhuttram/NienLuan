from django.contrib import admin
from sanpham.models import San_Pham,Loai_San_Pham,Chi_Tiet_San_Pham,Binh_Luan
from import_export.admin import ImportExportModelAdmin
# Register your models here.
class sanphamadmin(ImportExportModelAdmin):
    list_display = ['ten_san_pham','loai','gia','so_luong','anh_san_pham','mo_ta','trang_thai']
    
class loaiadmin(ImportExportModelAdmin):
    list_display = ['loai_ten','trang_thai']

class chitietadmin(admin.ModelAdmin):
    list_display = ['san_pham','ten','gia_khuyen_mai','khuyen_mai','trang_thai']  
    
class binhluan(admin.ModelAdmin):
    list_display = ['khach_hang','san_pham','noidung','create_at','update_at','trang_thai']  

admin.site.register(San_Pham,sanphamadmin)
admin.site.register(Loai_San_Pham,loaiadmin)
admin.site.register(Chi_Tiet_San_Pham,chitietadmin)
admin.site.register(Binh_Luan,binhluan)

