import re
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from khachhang.my_captcha import FormWithCaptcha
from django.contrib import messages

from sanpham.models import Loai_San_Pham
from .models import Khach_Hang
from rest_framework import status
from .forms import dangkyForm
from django.http import HttpResponsePermanentRedirect
from social_django.models import UserSocialAuth
from giohang.models import Gio_Hang
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from giohang.models import San_Pham_Trong_Gio
from dathang.models import Dat_Hang
from django.db.models import Count
# Create your views here
# quan tri
def viewkhachhang(request):
    #  lấy tất cả khách hàng với id lớn hơn 1
    khachhang = Khach_Hang.objects.filter(id__gt = '1')
    return render(request, 'pages/quantrikhachhang.html' , {'khachhang':khachhang} )        

def xoakhachhang(request, id):
    khachhang = Khach_Hang.objects.filter(id = id)
    khachhang.delete()
    return HttpResponsePermanentRedirect(request.META.get('HTTP_REFERER','/'))
        
#het quan tri    
def dangky(request):
    form = dangkyForm()
    if request.method == 'POST':
        form = dangkyForm(request.POST)
        # goi hàm kiểm tra
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('matkhau1')
            user = authenticate(request,username = username, password = password)
            login(request, user,backend='django.contrib.auth.backends.ModelBackend')
            return redirect('/')

    return render(request,  'pages/dangky.html', { 'form' : form})

# doi mat khau
@login_required(login_url = 'dangnhap')   
def doimatkhau(request):
    listloaisanphamall = Loai_San_Pham.objects.all()
    if request.user.is_authenticated:
        khachhang = Khach_Hang.objects.get(username = request.user)
        giohang = Gio_Hang.objects.filter(khach_hang = khachhang).last()
        if Gio_Hang.objects.filter(khach_hang =  request.user).exists():
            giohang = Gio_Hang.objects.get(khach_hang =  request.user)
            tongsanpham_tronggio = San_Pham_Trong_Gio.objects.filter(
                gio_hang = giohang).aggregate(
                    tong = Count('san_pham'))
    if request.method == 'POST':
        form1 = PasswordChangeForm(request.user, request.POST)
        if form1.is_valid():
            user = form1.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('/' )
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form1 = PasswordChangeForm(request.user)
    return render(request, 'pages/doimatkhau.html', {
        'form1': form1,
        'giohang':giohang,
        'listloaisanphamall':listloaisanphamall,
        'tongsanpham_tronggio':tongsanpham_tronggio
    })
    
# thong tin khach hang
@login_required(login_url = 'dangnhap')   
def thongtinkhachhang(request):
    tongsanpham_tronggio = 0 
    listloaisanphamall = Loai_San_Pham.objects.all()
    system_messages = messages.get_messages(request)
    for message in system_messages:
        pass
    if request.user.is_authenticated:
        khachhang = Khach_Hang.objects.get(username = request.user)
        if Gio_Hang.objects.filter(khach_hang =  request.user).exists():
            giohang = Gio_Hang.objects.get(khach_hang =  request.user)
            tongsanpham_tronggio = San_Pham_Trong_Gio.objects.filter(
                gio_hang = giohang).aggregate(
                    tong = Count('san_pham'))
        if 'submit' in request.POST:
            if request.method == 'POST':
                first_name = request.POST['first_name']
                last_name = request.POST['last_name']
                email = request.POST['emailthongtin']
               
                sdt = request.POST['sdt'] 
                diachi = request.POST['diachi']
                
                khachhang.first_name = first_name
                khachhang.last_name = last_name
                khachhang.email = email
                khachhang.so_dien_thoai = sdt
                khachhang.dia_chi = diachi
                khachhang.save()
                messages.success(request, 'Thành Công', fail_silently=False)
            else:
                return HttpResponseRedirect('/')
      
    return render(request, 'pages/thongtinkhachhang.html', {
        'khachhang':khachhang,
        'giohang':giohang,
        'listloaisanphamall':listloaisanphamall,
        'tongsanpham_tronggio':tongsanpham_tronggio
    })
    
