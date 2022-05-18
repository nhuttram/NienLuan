from django.contrib import admin
from .models import Dat_Hang
# Register your models here.
class dathangadmin(admin.ModelAdmin):
    list_display = ['khach_hang']
    

admin.site.register(Dat_Hang,dathangadmin)

