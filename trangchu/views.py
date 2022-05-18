from django.shortcuts import redirect, render
from django.http import HttpResponsePermanentRedirect, JsonResponse
from sanpham.models import Loai_San_Pham, San_Pham,Chi_Tiet_San_Pham,Binh_Luan
from giohang.models import Gio_Hang, San_Pham_Trong_Gio
from dathang.models import Dat_Hang
from django.db.models import Count,Sum
from django.views.generic import TemplateView 
from django.contrib.auth.mixins import LoginRequiredMixin
from dathang.models import Chi_Tiet_Dat_Hang
from social_django.models import UserSocialAuth
from khachhang.models import Khach_Hang

from django.core.mail import send_mail
from django.conf import settings
# Create your views here.  

 
def index(request):
    tongsanpham_tronggio = 0 
    giohang = 0    
    if request.user.is_authenticated:
        if Gio_Hang.objects.filter(khach_hang =  request.user).exists():
                giohang = Gio_Hang.objects.get(khach_hang =  request.user)
                tongsanpham_tronggio = San_Pham_Trong_Gio.objects.filter(gio_hang = giohang).aggregate(tong = Count('san_pham'))
        else:   
            ten =  Khach_Hang.objects.get(username = request.user )
            taogio = Gio_Hang.objects.create(khach_hang = ten)
            taogio.save()
            giohang = Gio_Hang.objects.get(khach_hang =  request.user)
            tongsanpham_tronggio = San_Pham_Trong_Gio.objects.filter(gio_hang=giohang).aggregate(tong = Count('san_pham'))
  
    listloaisanpham = Loai_San_Pham.objects.all().order_by('-id')[:10] 
    listloaisanphamall = Loai_San_Pham.objects.all()
    
    list8sanpham = San_Pham.objects.filter().order_by('-id')[:8] 
    
    listsanphamall = San_Pham.objects.filter().order_by('-id')[:15]
    
    if 'xemthem' in request.POST:
        listsanphamall = San_Pham.objects.filter().order_by('-id')[:]
        
    if 'term' in request.GET:
        qs = San_Pham.objects.filter(ten_san_pham__icontains = request.GET.get('term'))
        ten = list()
        for tensanpham in qs:
           ten.append(tensanpham.ten_san_pham)
        return JsonResponse(ten, safe=False)
    
    return render(request, 'pages/index.html', 
                  {'loaisanpham': listloaisanpham,
                   'listloaisanphamall':listloaisanphamall,
                   'giohang':giohang,
                   'sanpham': list8sanpham, 
                    'listsanphamall' : listsanphamall,
                   'tongsanpham_tronggio': tongsanpham_tronggio})

def chitietsanpham(request, id):
    tongsanpham_tronggio = 0     
    giohang = 0 
    if request.user.is_authenticated:
        if Gio_Hang.objects.filter(khach_hang =  request.user).exists():
                giohang = Gio_Hang.objects.get(khach_hang =  request.user)
                tongsanpham_tronggio = San_Pham_Trong_Gio.objects.filter(gio_hang = giohang).aggregate(tong = Count('san_pham'))       
        giohang = Gio_Hang.objects.get(khach_hang =  request.user)          
    
    listloaisanphamall = Loai_San_Pham.objects.all()
    sanpham = San_Pham.objects.get(id = id )
    
    if Chi_Tiet_Dat_Hang.objects.filter(san_pham = id).exists():
    
        soluongsp = Chi_Tiet_Dat_Hang.objects.filter(san_pham = id).aggregate(spban =Sum('so_luong')) 
        kho = int(sanpham.so_luong) - int(soluongsp['spban'])
    else:
        kho = int(sanpham.so_luong)
    

    sanphamchitiet = San_Pham.objects.filter(id = id)

    spcungloai = San_Pham.objects.filter(
        loai_id = sanpham.loai_id   
    ).exclude(id = id)
    
    binhluan = 0
    if Binh_Luan.objects.filter(san_pham = id).exists():
        binhluan = Binh_Luan.objects.filter(san_pham = id)
    if request.user.is_authenticated:   
        khach_hang = Khach_Hang.objects.get(username = request.user)
        if request.method == "POST":
            noidung = request.POST['noidung']
            binhluan1 = Binh_Luan.objects.create(khach_hang = khach_hang,
                                                san_pham = sanpham,
                                                noidung = noidung,
                                                )
            binhluan1.save()
       
    return render(request, 'pages/chitietsanpham.html', {'sanphamchitiet' : sanphamchitiet, 
                                                         'kho':kho,
                                                         'listloaisanphamall':listloaisanphamall,
                                                         'giohang' : giohang,
                                                         'sanpham': sanpham,
                                                         'binhluan':binhluan,
                                                         'sanphamcungloai': spcungloai, 
                                                         'tongsanpham_tronggio':tongsanpham_tronggio})


    
# tìm kiếm sản phẩm
def timkiem(request):
    tongsanpham_tronggio = 0
    giohang = 0
    listloaisanpham = Loai_San_Pham.objects.all()
    if request.user.is_authenticated:
        giohang = Gio_Hang.objects.get(khach_hang =  request.user)
        tongsanpham_tronggio = San_Pham_Trong_Gio.objects.filter(
            gio_hang=giohang).aggregate(
                tong = Count('san_pham'))
         
    if request.method == "POST":
        timkiem = request.POST['autotim']
        sanpham = San_Pham.objects.filter(
            ten_san_pham__icontains = timkiem
        ).prefetch_related('chitietsanpham1')[:8]
        
        listloaisp10 = Loai_San_Pham.objects.all().order_by('-id')[:10]
        
        loaisanpham = Loai_San_Pham.objects.filter()
        
        return render(request, 'pages/timkiem.html', 
                      {'timkiem' : timkiem ,
                       'listloaisp10':listloaisp10,
                       'listloaisanphamall' : loaisanpham,
                       'giohang' :giohang, 
                       'sanpham': sanpham, 
                       'loaisanpham' : listloaisanpham,
                       'tongsanpham_tronggio':tongsanpham_tronggio })
    else:
         return HttpResponsePermanentRedirect('/')
     
def loaisanpham(request, id):
        tongsanpham_tronggio = 0
        loaisanphamtheoID = Loai_San_Pham.objects.get(id = id)
        
        loaisanpham = Loai_San_Pham.objects.filter()
        
        listloaisp10 =  Loai_San_Pham.objects.filter().order_by('-id')[:10]
        
        sanpham = San_Pham.objects.filter(loai = loaisanphamtheoID)  
        if request.user.is_authenticated:
            giohang = Gio_Hang.objects.get(khach_hang =  request.user)
            tongsanpham_tronggio = San_Pham_Trong_Gio.objects.filter(
                gio_hang = giohang).aggregate(
                    tong = Count('san_pham')) 
        
        return render(request, 'pages/loaisanpham.html', {'sanpham': sanpham, 
                                                          'listloaisanphamall' : loaisanpham,
                                                          'tongsanpham_tronggio':tongsanpham_tronggio,
                                                          'loaisanphamtheoID':loaisanphamtheoID,
                                                          'listloaisp10':listloaisp10,
                                                          })


def xoabl(request,id):
    binhluan = Binh_Luan.objects.get(id = id)
    binhluan.delete()
    return HttpResponsePermanentRedirect(request.META.get('HTTP_REFERER','/')) 
    

#gởi gamil tự động
def email(request):
    if request.method == 'POST':
        email = request.POST['email']
        fname = request.POST['fname']
        lname = request.POST['lname']
        tieude = request.POST['tieude']
        message = request.POST['message']
        
        subject = tieude
        message = fname + lname + message
        email_from = settings.EMAIL_HOST_USER
        recipient_list = [email]
        send_mail( subject, message, email_from, recipient_list )
    return redirect('/')

# lỗi
def handle_not_found(request,exception):
    return render(request,'loi.html')

def handle_server_error(request):
    return render(request,'loi.html')