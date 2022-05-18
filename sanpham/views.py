from email import message
from operator import imod
from django.forms.forms import Form
from django.shortcuts import redirect, render
from django.http import HttpResponse, response
from .forms import uploadMulti
from .models import Loai_San_Pham, San_Pham,Chi_Tiet_San_Pham
import datetime
import xlwt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
# Paginator
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .resources import LoaiReource,SanPhamReource
from tablib import Dataset

# hien thi danh sach loai
@permission_required('auth.view_user') 
@login_required(login_url = 'dangnhap')
def get_loai(request):
    # lấy dữ lieu trong bảng
    deparment_list = Loai_San_Pham.objects.filter().order_by('id')
    return render(request, 'pages/loaihang.html',
                  {'loai' : deparment_list})

# hien thi form
@permission_required('auth.view_user') 
@login_required(login_url = 'dangnhap')
def get_loaihangform(request):
    return render(request, 'pages/themloai.html')
# them lai
@permission_required('auth.view_user') 
@login_required(login_url = 'dangnhap')
def add_loai(request):
    if request.method == 'POST':
        if 'tenloaihang' in request.POST:
            loai_ten = request.POST['tenloaihang']
            print(loai_ten)
            themloai = Loai_San_Pham.objects.create(loai_ten = loai_ten)
            themloai.save()
            return redirect('quantri/loaihang/')
        elif 'file' in request.POST:
            loai_recource = LoaiReource()
            dataset = Dataset()
            new_loai = request.FILES['loai']
            if not new_loai.name.endswith('xlsx'):
                alert=1
                return render(request,'pages/themloai.html',{'alert':alert})
            themloai = dataset.load(new_loai.read(), format = 'xlsx') 
            for data in themloai:
                value = Loai_San_Pham(
                    data[0],
                    data[1],
                    trang_thai=1,
                )
                value.save()
            return redirect('quantri/loaihang/')
        return  render(request,"pages/themloai.html")
    
    else:
        return render(request,"pages/themloai.html")
    # else:
    #     return render(request, 'loi.html')
    
        
# sua loai
@permission_required('auth.view_user') 
@login_required(login_url = 'dangnhap')
def sua_loai(request, id):
    id = Loai_San_Pham.objects.get(id = id)
    if request.method == 'POST':
        loai_ten = request.POST['tenloaihang'] 
        id.loai_ten = loai_ten
        id.save()
        return redirect('/quantri/loaihang/')
    
    return render(request, 'pages/sualoai.html', 
                  {'loai_ten' : id})
# xoa loai
@permission_required('auth.view_user') 
@login_required(login_url = 'dangnhap')
def xoa_loai(request, id):
    xoa_loai =  Loai_San_Pham.objects.get(id = id)
    xoa_loai.delete()
    return redirect('/quantri/loaihang/')

#  san pham 
# hien thi danh sach các sản phẩm
@permission_required('auth.view_user') 
@login_required(login_url = 'dangnhap')
def get_sanpham(request): 
    # Paging
    if request.method == 'POST':
        ten = request.POST['tensanpham']
        if San_Pham.objects.filter(ten_san_pham__contains = ten ).exists():
            deparment_list = San_Pham.objects.filter(ten_san_pham__contains = ten )
        else:
            deparment_list = ''
    else:
         # lấy dữ lieu trong bảng
        deparment_list = San_Pham.objects.all().order_by('-id')
    
    paginator = Paginator(deparment_list, 4)
    page = request.GET.get('page', 1)
    try:
        orders_paged = paginator.page(page)
    except PageNotAnInteger:
        orders_paged = paginator.page(1)
    except EmptyPage:
        orders_paged = paginator.page(paginator.num_pages)

    return render(request, 'pages/sanpham.html' , 
                  {'sanpham_list' : deparment_list,
                   "orders": orders_paged } )

# hien thi form nhap san pham
@permission_required('auth.view_user') 
@login_required(login_url = 'dangnhap')
def get_sanphamform(request):
    loai = Loai_San_Pham.objects.filter()
    return render(request, 'pages/themsanphamform.html', 
                  {'loai' : loai ,})
# them san pham
@permission_required('auth.view_user') 
@login_required(login_url = 'dangnhap')
def add_sanpham(request):
    if request.method == 'POST':
        if 'tensanpham' in request.POST:
            tensanpham = request.POST['tensanpham']
            loai = request.POST['loai']
            id = Loai_San_Pham.objects.get(id = loai)
            soluong = request.POST['soluong']
            gia = request.POST['gia']
            anh =  request.FILES['images']
            mota =  request.POST['mota']
            themsanpham = San_Pham.objects.create(ten_san_pham = tensanpham,
                                                mo_ta = mota,
                                                loai = id,
                                                gia=gia,
                                                so_luong=soluong,
                                                anh_san_pham=anh)
            themsanpham.save()
            return redirect('quantri/sanpham.html')
        elif 'filesp' in request.POST:
                sp_recource = SanPhamReource()
                dataset = Dataset()
                new_sp = request.FILES['filesanpham'] 
                if not new_sp.name.endswith('xlsx'):
                    alert=1
                    return render(request,'pages/themloai.html',{'alert':alert})
                themsanphamfile = dataset.load(new_sp.read(), format = 'xlsx') 
                for data in themsanphamfile:
                    value = San_Pham(
                        data[0],
                        data[1],
                        data[2],
                        data[3],
                        data[4],
                        data[5],
                        data[6],
                        trang_thai=1,
                    )
                    value.save()
                return redirect('quantri/sanpham.html')
    return  render(request,"pages/themsanphamform.html")
            
    
# xuất file sản phẩm
@permission_required('auth.view_user') 
@login_required(login_url = 'dangnhap')
def xuatfilesp(request):
    response = HttpResponse(content_type = "application/ms-excel")
    response['Content-Disposition'] = 'attachment; filename=San_Pham'+ \
        str(datetime.datetime.now())+'.xls'
    wb = xlwt.Workbook(encoding='utf-8')
    ws = wb.add_sheet('San_Pham')
    row_num = 0
    font_style = xlwt.XFStyle()
    font_style.font.old = True
    colums = ['id','ten_san_pham','loai','gia','so_luong','anh_san_pham','mo_ta']
    for col_num in range(len(colums)):
        ws.write(row_num,col_num,colums[col_num],font_style)
        
    font_style = xlwt.XFStyle()
    rows = San_Pham.objects.filter().values_list(
        'id','ten_san_pham','loai','gia','so_luong','anh_san_pham','mo_ta'
    )
    for row in rows:
        row_num += 1
        for col_num in range(len(row)):
            ws.write(row_num, col_num, str(row[col_num]),font_style)
    wb.save(response) 
    return response

# xoa san pham 
@permission_required('auth.view_user') 
@login_required(login_url = 'dangnhap')
def xoa_san_pham(request, id):
    xoa_loai =  San_Pham.objects.get(id = id)
    xoa_loai.delete()
    return redirect('/quantri/sanpham.html')

# sua san pham
@permission_required('auth.view_user') 
@login_required(login_url = 'dangnhap')
def sua_san_pham(request, id):
    id_sanpham = San_Pham.objects.get(id = id)
    loai = Loai_San_Pham.objects.filter()
    if request.method == 'POST':
        tensanpham = request.POST['tensanpham']
        loai = request.POST['loai']
        id = Loai_San_Pham.objects.get(id = loai)
        soluong = request.POST['soluong']
        gia = request.POST['gia']
        mota =  request.POST['mota'] 
        id_sanpham.ten_san_pham = tensanpham
        id_sanpham.mo_ta = mota
        id_sanpham.loai = id
        id_sanpham.gia = gia
        id_sanpham.so_luong = soluong
        
        if  request.FILES.get('anh', False):
            anh = request.FILES['anh']
            id_sanpham.anh_san_pham = anh
        else:
            anh =  request.POST['anh1']
            id_sanpham.anh_san_pham = anh
            
        id_sanpham.save()
        return redirect('/quantri/sanpham.html')
    
    return render(request, 'pages/suasanpham.html',
                  {'san_pham' : id_sanpham ,'loai' : loai})


# giảm giá 
@permission_required('auth.view_user') 
@login_required(login_url = 'dangnhap')
def giamgia(request):
     # Paging
    if request.method == 'POST':
        ten = request.POST['tensanpham']
        deparment_list = San_Pham.objects.filter(ten_san_pham__contains = ten )
    else:
         # lấy dữ lieu trong bảng
        deparment_list = Chi_Tiet_San_Pham.objects.all().order_by('-id')
    
    paginator = Paginator(deparment_list, 4 )
    page = request.GET.get('page', 1)
    try:
        orders_paged = paginator.page(page)
    except PageNotAnInteger:
        orders_paged = paginator.page(1)
    except EmptyPage:
        orders_paged = paginator.page(paginator.num_pages)
    return render(request,'pages/giamgia.html',
                  {"orders": orders_paged})

@permission_required('auth.view_user') 
@login_required(login_url = 'dangnhap')
def giam_gia_san_pham(request, id):
    id_sanpham = San_Pham.objects.get(id = id)
    id_giamgia = 0
    if Chi_Tiet_San_Pham.objects.filter(san_pham = id_sanpham).exists():
        id_giamgia = Chi_Tiet_San_Pham.objects.get(san_pham = id_sanpham) 
    if request.method == 'POST':
        gia_giam = id_sanpham.gia - (id_sanpham.gia*(int(request.POST['giamgia'])/ 100))
       
       
        if Chi_Tiet_San_Pham.objects.filter(san_pham = id_sanpham).exists():
            suagiamgia = Chi_Tiet_San_Pham.objects.get(san_pham = id_sanpham)
            suagiamgia.ten = request.POST['tengiamgia']
            suagiamgia.gia_khuyen_mai =gia_giam
            suagiamgia.khuyen_mai = request.POST['giamgia']
            suagiamgia.save()
            return redirect('/quantri/giamgia/')
        else:
            giamgia = Chi_Tiet_San_Pham.objects.create(san_pham = id_sanpham,
                                                    ten = request.POST['tengiamgia'],
                                                    gia_khuyen_mai = gia_giam,
                                                    khuyen_mai = request.POST['giamgia'],
                                                   )
            giamgia.save()
            return redirect('/quantri/giamgia/') 
    
    return render(request,'pages/themgiamgia.html',{'san_pham' : id_sanpham ,'id_giamgia':id_giamgia})

@permission_required('auth.view_user') 
@login_required(login_url = 'dangnhap')
def xoa_giam_gia(request, id):
    id_xoa = Chi_Tiet_San_Pham.objects.get(id = id)
    id_xoa.delete()
    
    return redirect('/quantri/giamgia/')