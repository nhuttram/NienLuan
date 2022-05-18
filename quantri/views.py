import datetime
from xmlrpc.client import DateTime
from django.db.models import Sum,Count
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponsePermanentRedirect, response
from khachhang.models import Khach_Hang
from sanpham.models import Loai_San_Pham as loaisanpham
from sanpham.models import  San_Pham
# Create your views here.
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from dathang.models import Chi_Tiet_Dat_Hang, Dat_Hang

# Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

@permission_required('auth.view_user') 
@login_required(login_url = 'dangnhap')
def index(request):
    danhthu = 0
    sodon = 0
    donhangchuaxacnhan = ''
    donhang = ''
    donhangthanhtoanpaypal = ''
    sanphamkho = ''
    if Dat_Hang.objects.filter().exists(): 
        danhthu = Dat_Hang.objects.all().aggregate(danhthu = Sum('tongtien')) 
        sodon = Dat_Hang.objects.all().aggregate(sodon = Count('tongtien')) 
        donhang = Dat_Hang.objects.all().order_by('-id')[:10]
        
        donhangchuaxacnhan = Dat_Hang.objects.filter(trang_thai_dat_hang = 'chua_xac_nhan').order_by('id')[:10]
        
        donhangthanhtoanpaypal = Dat_Hang.objects.filter(hinh_thuc = 'paypal',trang_thai=1).order_by('id')[:10]
    
        sanphamkho = ''
        soluongsp = (Chi_Tiet_Dat_Hang.objects
        .values('san_pham')
        .annotate(spban=Sum('so_luong'))
        .order_by()
            )  
        idsphet = []
        for soluongsp in soluongsp:
            idsp = soluongsp['san_pham']
            slban = soluongsp['spban']
            slsanpham = San_Pham.objects.get(id = int(idsp))   
            if int(slsanpham.so_luong) - int(slban) < 3:
                idsphet.append(idsp)
                
        sanphamkho = San_Pham.objects.raw("SELECT * FROM sanpham_san_pham WHERE sanpham_san_pham.id IN %s LIMIT 10", [tuple(idsphet)])
    

            
            
    return render(request, 'pages/trangchu.html', {
                        'danhthu' : danhthu,
                        'sodon' : sodon,
                        'donhang':donhang,
                        'donhangchuaxacnhan':donhangchuaxacnhan,
                        'donhangthanhtoanpaypal':donhangthanhtoanpaypal,
                        'sanphamkho': sanphamkho,
                                }
                  )

@permission_required('auth.view_user') 
@login_required(login_url = 'dangnhap')
def quantridonhang(request):
    
    # Paging
    if request.method == 'POST':
        #ten = request.POST['tensanpham']
       # deparment_list = Dat_Hang.objects.raw('SELECT *,GROUP_CONCAT(sanpham_San_Pham.ten_san_pham,"(",giohang_San_Pham_Trong_Gio.so_luong,")"  ORDER BY giohang_San_Pham_Trong_Gio.gio_hang_id ASC SEPARATOR ", ") AS ten_sp FROM dathang_Dat_Hang JOIN giohang_Gio_Hang ON dathang_Dat_Hang.gio_hang_id=giohang_Gio_Hang.id JOIN giohang_San_Pham_Trong_Gio ON giohang_Gio_Hang.id = giohang_San_Pham_Trong_Gio.gio_hang_id JOIN sanpham_San_Pham ON  giohang_San_Pham_Trong_Gio.san_pham_id = sanpham_San_Pham.id WHERE 1 GROUP BY giohang_San_Pham_Trong_Gio.gio_hang_id ORDER BY giohang_San_Pham_Trong_Gio.gio_hang_id DESC')
        deparment_list = Dat_Hang.objects.all()
    else:
        # lấy dữ lieu trong bảng
       # deparment_list = Dat_Hang.objects.raw('SELECT *,GROUP_CONCAT(sanpham_San_Pham.ten_san_pham,"(",giohang_San_Pham_Trong_Gio.so_luong,")"  ORDER BY giohang_San_Pham_Trong_Gio.gio_hang_id ASC SEPARATOR ", ") AS ten_sp FROM dathang_Dat_Hang JOIN giohang_Gio_Hang ON dathang_Dat_Hang.gio_hang_id=giohang_Gio_Hang.id JOIN giohang_San_Pham_Trong_Gio ON giohang_Gio_Hang.id = giohang_San_Pham_Trong_Gio.gio_hang_id JOIN sanpham_San_Pham ON  giohang_San_Pham_Trong_Gio.san_pham_id = sanpham_San_Pham.id WHERE 1 GROUP BY giohang_San_Pham_Trong_Gio.gio_hang_id ORDER BY giohang_San_Pham_Trong_Gio.gio_hang_id DESC') 
        deparment_list = Dat_Hang.objects.filter()
    paginator = Paginator(deparment_list, 9)
    page = request.GET.get('page', 1)
    try:
        orders_paged = paginator.page(page)
    except PageNotAnInteger:
        orders_paged = paginator.page(1)
    except EmptyPage:
        orders_paged = paginator.page(paginator.num_pages)
    
    #dathang = Dat_Hang.objects.raw('SELECT *,GROUP_CONCAT(sanpham_San_Pham.ten_san_pham,"(",giohang_San_Pham_Trong_Gio.so_luong,")"  ORDER BY giohang_San_Pham_Trong_Gio.gio_hang_id ASC SEPARATOR ", ") AS ten_sp FROM dathang_Dat_Hang JOIN giohang_Gio_Hang ON dathang_Dat_Hang.gio_hang_id=giohang_Gio_Hang.id JOIN giohang_San_Pham_Trong_Gio ON giohang_Gio_Hang.id = giohang_San_Pham_Trong_Gio.gio_hang_id JOIN sanpham_San_Pham ON  giohang_San_Pham_Trong_Gio.san_pham_id = sanpham_San_Pham.id WHERE 1 GROUP BY giohang_San_Pham_Trong_Gio.gio_hang_id ORDER BY giohang_San_Pham_Trong_Gio.gio_hang_id DESC')
    
    
    
    if request.method == 'POST':
        id_don =  request.POST['id_don']
        trang_thai_dat_hang = request.POST['trang_thai_dat_hang']
        
        if trang_thai_dat_hang == '1':
            doitrangthai = Dat_Hang.objects.get(id = id_don)
            doitrangthai.trang_thai_dat_hang = 'da_xac_nhan'
            doitrangthai.update_at = datetime.date.today()
            doitrangthai.save()
        elif trang_thai_dat_hang == '2':
            doitrangthai = Dat_Hang.objects.get(id = id_don)
            doitrangthai.trang_thai_dat_hang = 'da_giao_hang'
            doitrangthai.update_at = datetime.date.today()
            doitrangthai.save()
        elif trang_thai_dat_hang == '3':
            doitrangthai = Dat_Hang.objects.get(id = id_don)
            doitrangthai.trang_thai_dat_hang = 'huy_don'
            doitrangthai.update_at = datetime.date.today()
            doitrangthai.save()
        
            
    return render(request, 'pages/quantridonhang.html', 
                  {'dathang' : deparment_list,
                   "orders": orders_paged,})
    

@permission_required('auth.view_user') 
@login_required(login_url = 'dangnhap')
def quantrichitietdon(request , id):
    
    dat_hang = Dat_Hang.objects.get(id = id)
    chitiet_donhang = Chi_Tiet_Dat_Hang.objects.filter(dat_hang = dat_hang )
    khachhang = Khach_Hang.objects.get(id = dat_hang.khach_hang.id)
    return render(request, 'pages/quantridonhangchitiet.html', 
                  {'dat_hang' : dat_hang,
                   'chitiet_donhang' : chitiet_donhang,
                   'khachhang':khachhang,
                   })
    

@permission_required('auth.view_user') 
@login_required(login_url = 'dangnhap')
def quantrihuydon(request , id_huydon):
    huy_don = Dat_Hang.objects.get(id = id_huydon)
    huy_don.trang_thai_dat_hang = 'huy_don'
    huy_don.save()
    
    return redirect('quantridonhang') 

def quantrixoadon(request , id_huydon):
    xoa_don = Dat_Hang.objects.get(id = id_huydon)
    xoa_don.delete()
    
    return redirect('quantridonhang') 
  