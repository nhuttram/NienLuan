from asyncio.windows_events import NULL
import datetime
from xmlrpc.client import DateTime
from django.shortcuts import render,redirect
from giohang.models import Gio_Hang, San_Pham_Trong_Gio
from sanpham.models import San_Pham
from khachhang.models import Khach_Hang
from .models import Chi_Tiet_Dat_Hang, Dat_Hang
from django.db.models import Count, Sum
from django.http import HttpResponsePermanentRedirect,HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
# Create your views here.

def dat_hang(request, id):
    giohang = Gio_Hang.objects.get(
        id = id
    )
    id_gio = id
    khachhang = Khach_Hang.objects.get(
        username = request.user
    )
    sanphamtronggio = San_Pham_Trong_Gio.objects.filter(
        gio_hang = giohang
    )
    sanpham_gio = San_Pham_Trong_Gio.objects.filter(
        gio_hang_id = giohang.id
    ).select_related('san_pham')
    tien = 0
    kq1 = 0
    kq2 = 0
    tong = 0
    for sp in sanpham_gio:  
        khuyenmai = San_Pham.objects.raw(
            'SELECT * FROM sanpham_san_pham LEFT JOIN sanpham_chi_tiet_san_pham ON sanpham_san_pham.id=sanpham_chi_tiet_san_pham.san_pham_id WHERE sanpham_san_pham.id = %s',[sp.san_pham.id]
        )
        for khuyenmai in khuyenmai:
            if khuyenmai.gia_khuyen_mai !=  None:
                kq1 += float(sp.so_luong) * float(khuyenmai.gia_khuyen_mai)
            if khuyenmai.gia_khuyen_mai ==  None:
                kq2 += float(sp.so_luong) * float(khuyenmai.gia)    
            tien  = kq1 + kq2
    tong = tien + 25000
    tongUSA = tong/23000
    if request.user.is_authenticated:
        khachhang = Khach_Hang.objects.get(username = request.user)
        if 'submit' in request.POST:
            if request.method == 'POST':
                email = request.POST['email']
                sdt = request.POST['sdt'] 
                diachi = request.POST['diachi']
                khachhang.email = email
                khachhang.so_dien_thoai = sdt
                khachhang.dia_chi = diachi
                khachhang.save()
                messages.info(request, 'Cập Nhật Thành Công Thông Tin Cá Nhân!', fail_silently=False)
            else:
                return HttpResponseRedirect('/')
   
    return render(request, 'pages/dat_hang.html', {'tong': tong,
                                                   'id_gio':id_gio,
                                                   'khachhang':khachhang,
                                                   'tongUSA':tongUSA,
                                                   'sanpham_gio':sanpham_gio})
    
@csrf_exempt   
def thanh_toan_pay_pal(request):
    if request.method == 'POST':
        id = request.POST['id_giohang']
    sanpham_gio = San_Pham_Trong_Gio.objects.filter(
        gio_hang_id = id
    ).select_related('san_pham')
    
    tien = 0
    kq1 = 0
    kq2 = 0
    tong = 0
    tong_giam =0
    ten =  Khach_Hang.objects.get(username = request.user )
    dat_hang = Dat_Hang.objects.create(khach_hang = ten,
                                    hinh_thuc =  'paypal',
                                    trang_thai = '1',
                                    tongtien = 0)
    dat_hang.save()
   
    for sp in sanpham_gio:  
        khuyenmai = San_Pham.objects.raw(
            'SELECT * FROM sanpham_san_pham LEFT JOIN sanpham_chi_tiet_san_pham ON sanpham_san_pham.id=sanpham_chi_tiet_san_pham.san_pham_id WHERE sanpham_san_pham.id = %s',[sp.san_pham.id]
        )
        id_sanpham = San_Pham.objects.get(id = sp.san_pham.id )
       
        for khuyenmai in khuyenmai:
            if khuyenmai.gia_khuyen_mai !=  None:
                kq1 += float(sp.so_luong) * float(khuyenmai.gia_khuyen_mai)
            if khuyenmai.gia_khuyen_mai ==  None:
                kq2 += float(sp.so_luong) * float(khuyenmai.gia)    
            tien  = kq1 + kq2
            
            id_dat_hang = Dat_Hang.objects.get(khach_hang = ten, tongtien = 0)
            
            chi_tiet_dat_hang = Chi_Tiet_Dat_Hang.objects.create(dat_hang = id_dat_hang,
                                                        san_pham = id_sanpham,
                                                        so_luong  = sp.so_luong,
                                                        giam_gia = khuyenmai.khuyen_mai)
            chi_tiet_dat_hang.save()
          
    tong = tien + 25000
    
    update_tongtien = Dat_Hang.objects.get(khach_hang = ten, tongtien = 0)
    update_tongtien.tongtien = tong
    update_tongtien.save()
    
    delectsp_gio = San_Pham_Trong_Gio.objects.filter(gio_hang = id )
    delectsp_gio.delete()
   
    update_gio = Gio_Hang.objects.get(khach_hang = ten)
    update_gio.delete()
    
    email = ten.email
    tieude = "Thanh toán hóa đơn - TmN_Shop"
    message = " Hóa đơn của bạn đã được đặt hàng thành công! \n Hình thức: Pay_Pal \n Bạn sẽ được gọi điện xác nhận đơn hàng vào thời giang sớm nhất \n Cảm ơn bạn đã sử dụng dịch vụ của chúng tôi."
        
    subject = tieude
    message = message
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail( subject, message, email_from, recipient_list )
    
    return redirect('/trangchu/khachhang/donhang.html')
    # return HttpResponsePermanentRedirect('/donhang') 

def thanh_toan_truc_tiep(request ,id):
    sanpham_gio = San_Pham_Trong_Gio.objects.filter(
        gio_hang_id = id
    ).select_related('san_pham')
    
    tien = 0
    kq1 = 0
    kq2 = 0
    tong = 0
    tong_giam =0
    ten =  Khach_Hang.objects.get(username = request.user )
    
    dat_hang = Dat_Hang.objects.create(khach_hang = ten,
                                        tongtien = 0)
    dat_hang.save()
   
    for sp in sanpham_gio:  
        khuyenmai = San_Pham.objects.raw(
            'SELECT * FROM sanpham_san_pham LEFT JOIN sanpham_chi_tiet_san_pham ON sanpham_san_pham.id=sanpham_chi_tiet_san_pham.san_pham_id WHERE sanpham_san_pham.id = %s',[sp.san_pham.id]
        )
        id_sanpham = San_Pham.objects.get(id = sp.san_pham.id )
       
        for khuyenmai in khuyenmai:
            if khuyenmai.gia_khuyen_mai !=  None:
                kq1 += float(sp.so_luong) * float(khuyenmai.gia_khuyen_mai)
            if khuyenmai.gia_khuyen_mai ==  None:
                kq2 += float(sp.so_luong) * float(khuyenmai.gia)    
            tien  = kq1 + kq2
            
            id_dat_hang = Dat_Hang.objects.get(khach_hang = ten, tongtien = 0)
            
            chi_tiet_dat_hang = Chi_Tiet_Dat_Hang.objects.create(dat_hang = id_dat_hang,
                                                        san_pham = id_sanpham,
                                                        so_luong  = sp.so_luong,
                                                        giam_gia = khuyenmai.khuyen_mai)
            chi_tiet_dat_hang.save()
          
    tong = tien + 25000
    
    update_tongtien = Dat_Hang.objects.get(khach_hang = ten, tongtien = 0)
    update_tongtien.tongtien = tong
    update_tongtien.save()
    
    delectsp_gio = San_Pham_Trong_Gio.objects.filter(gio_hang = id )
    delectsp_gio.delete()
   
    update_gio = Gio_Hang.objects.get(khach_hang = ten)
    update_gio.delete()
    
    email = ten.email
    tieude = "Thanh toán hóa đơn - TmN_Shop"
    message = " Hóa đơn của bạn đã được đặt hàng thành công! \n Hình thức: Thanh toán trực tiêp \n Bạn sẽ được gọi điện xác nhận đơn hàng vào thời giang sớm nhất \n Cảm ơn bạn đã sử dụng dịch vụ của chúng tôi."
        
    subject = tieude
    message = message
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail( subject, message, email_from, recipient_list )
   
    return redirect('/trangchu/khachhang/donhang.html')
    
    
@login_required(login_url = 'dangnhap')   
def donhang(request):
    khachhang = Khach_Hang.objects.get(username = request.user)
    # dathang = Dat_Hang.objects.raw('SELECT *,GROUP_CONCAT(sanpham_San_Pham.ten_san_pham, " " ,"(",giohang_San_Pham_Trong_Gio.so_luong, ")"  ORDER BY giohang_San_Pham_Trong_Gio.gio_hang_id ASC SEPARATOR " , ") AS ten_sp FROM dathang_Dat_Hang JOIN giohang_Gio_Hang ON dathang_Dat_Hang.gio_hang_id=giohang_Gio_Hang.id JOIN giohang_San_Pham_Trong_Gio ON giohang_Gio_Hang.id = giohang_San_Pham_Trong_Gio.gio_hang_id JOIN sanpham_San_Pham ON  giohang_San_Pham_Trong_Gio.san_pham_id = sanpham_San_Pham.id    WHERE dathang_Dat_Hang.khach_hang_id = %s GROUP BY giohang_San_Pham_Trong_Gio.gio_hang_id ORDER BY giohang_San_Pham_Trong_Gio.gio_hang_id DESC', [khachhang.id])
    
    if Dat_Hang.objects.filter(khach_hang = khachhang).exists():
        dathang = Dat_Hang.objects.filter(khach_hang = khachhang)
    else:
        dathang = ''
    giohang = Gio_Hang.objects.filter(khach_hang = khachhang).last()
    tongsanpham_tronggio = San_Pham_Trong_Gio.objects.filter(
            gio_hang=giohang).aggregate(
                tong = Count('san_pham'))
   
    return render(request, 'pages/khachhang_donhang.html', {
        'dathang': dathang,
        'giohang':giohang,
        'tongsanpham_tronggio': tongsanpham_tronggio,
    })
     
     
def chitiet_donhang(request , id):
    khachhang = Khach_Hang.objects.get(username = request.user)
    giohang = Gio_Hang.objects.filter(khach_hang = khachhang).last()
    tongsanpham_tronggio = San_Pham_Trong_Gio.objects.filter(
            gio_hang=giohang).aggregate(
                tong = Count('san_pham'))
   
   
    dathang1 = Dat_Hang.objects.get(id = id)
    chitietdathang = Chi_Tiet_Dat_Hang.objects.filter(dat_hang = dathang1)
    return render(request, 'pages/chitiet_donhang.html', {
        'dathang1': dathang1,
        'giohang':giohang,
        'chitietdathang':chitietdathang,
        'tongsanpham_tronggio':tongsanpham_tronggio
       
    })   



    
def huydon(request, id_huydon):
    huy_don = Dat_Hang.objects.get(id = id_huydon)
    huy_don.trang_thai_dat_hang = 'huy_don'
    huy_don.save()
    
    return redirect('/trangchu/khachhang/donhang.html')