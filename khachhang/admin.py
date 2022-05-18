from django.contrib import admin
from .models import Khach_Hang

# Register your models here.
class adminKhach_Hang(admin.ModelAdmin):
    list_display = ['username','password','email']
    
admin.site.register(Khach_Hang,adminKhach_Hang)