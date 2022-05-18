from asyncio.windows_events import NULL
from cgi import print_form
from xmlrpc.client import boolean
from django.db.models import Count, Sum
from django.shortcuts import redirect, render
from django.http.response import HttpResponsePermanentRedirect
from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy
from khachhang.models import Khach_Hang
from dathang.models import Dat_Hang
from sanpham.models import Loai_San_Pham, San_Pham,Chi_Tiet_San_Pham
from giohang.models import Gio_Hang, San_Pham_Trong_Gio
from django.contrib.auth.decorators import login_required
from dathang.models import Chi_Tiet_Dat_Hang
from django.contrib import messages
# Create your views here.

    

@login_required(login_url = 'dangnhap')   
def giohang(request, id_giohang): 
    listloaisanphamall = Loai_San_Pham.objects.all()
    #  lay thong tin khach hang
    giohang = Gio_Hang.objects.get(
        id = id_giohang
        )
  
    
    # goi san pham trong gio qua client
    sanpham_gio = San_Pham_Trong_Gio.objects.filter(
        gio_hang_id = giohang.id
    ).select_related('san_pham')
   
    # tinh so luong san pham
    tong_spgio = San_Pham_Trong_Gio.objects.filter(
        gio_hang = giohang
        ).aggregate(Sum('so_luong')
                    )  
    tongsanpham_tronggio = San_Pham_Trong_Gio.objects.filter(
            gio_hang=giohang).aggregate(
                tong = Count('san_pham'))
    tien = 0
    kq1 = 0
    kq2 = 0
    tong = 0
    tong_giam =0
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
   
    
    if request.method == 'POST':
        if 'soluong' in request.POST:
             if request.POST['soluong']:
                soluong = request.POST['soluong']
                sanpham_a = San_Pham.objects.get(id = request.POST['idsanphamtronggio']) 


                if Chi_Tiet_Dat_Hang.objects.filter(san_pham = request.POST['idsanphamtronggio']).exists():
                    soluongsp = Chi_Tiet_Dat_Hang.objects.filter(san_pham = request.POST['idsanphamtronggio']).aggregate(spban =Sum('so_luong'))
                    kho = int(sanpham_a.so_luong) - int(soluongsp['spban'])
                else:
                     kho = int(sanpham_a.so_luong) 
        
                if int(soluong) > kho: 
                    messages.error(request, 'Số Lượng Sản Phẩm Trong Kho Không Đủ')
                    return  HttpResponseRedirect(request.path,{'sanpham_a':sanpham_a})
                else:
                    
                    sanphamtronggio = San_Pham_Trong_Gio.objects.get(gio_hang = request.POST['id_giohang'], san_pham = sanpham_a)
                    sanphamtronggio.so_luong = soluong
                    sanphamtronggio.save()
                    return HttpResponsePermanentRedirect(request.META.get('HTTP_REFERER','/'))
    return render(request, 'pages/giohang.html', {'giohang': giohang,
                                                  'sanpham_gio' : sanpham_gio,
                                                  'tong_spgio':tong_spgio,
                                                  'listloaisanphamall':listloaisanphamall,
                                                  'tongsanpham_tronggio':tongsanpham_tronggio,
                                                  'kqtongtien' : tien,
                                                  'tong': tong, 
                                                  'tong_giam':tong_giam,
                                                  })
def xoagio(request, idgio, san_pham): 
    sanpham_a = San_Pham.objects.get(id =  san_pham)
    sanphamtronggio = San_Pham_Trong_Gio.objects.get(id = idgio, san_pham = sanpham_a)
    sanphamtronggio.delete()
    return HttpResponsePermanentRedirect(request.META.get('HTTP_REFERER','/'))
       
def themgiohang(request,id): 
    id = San_Pham.objects.get(id = id)

    soluongsp = Chi_Tiet_Dat_Hang.objects.filter(san_pham = id).aggregate(spban =Sum('so_luong'))
    if request.method == 'POST':
        if request.user.is_authenticated:
            id_giohang = Gio_Hang.objects.get(khach_hang =  request.user)
            print(id_giohang)
            if San_Pham_Trong_Gio.objects.filter(san_pham = id, gio_hang = id_giohang).exists() == False:
                if request.POST.get('soluong', False):
                    soluong = request.POST['soluong']
                    themvaogio = San_Pham_Trong_Gio.objects.create(gio_hang = id_giohang,
                                                                san_pham =id,
                                                                so_luong = soluong)
                    themvaogio.save()
                else:
                    soluong = 1
  
                    themvaogio = San_Pham_Trong_Gio.objects.create(gio_hang = id_giohang,
                                                                san_pham =id,
                                                                so_luong = soluong)
                    themvaogio.save()
            else:
                id_gio =  San_Pham_Trong_Gio.objects.get(san_pham = id, gio_hang = id_giohang )
                if request.POST.get('soluong', False):
                    soluong = request.POST['soluong']
                    
                    tongso = int(soluong) + int(id_gio.so_luong)
                    
                    id_gio.so_luong = tongso
                    id_gio.save()
                    
                else:
                    soluong = 1
                    id_gio.save()
                    
          
    return HttpResponsePermanentRedirect(request.META.get('HTTP_REFERER','/'))


    
        
        
    


           
  
    