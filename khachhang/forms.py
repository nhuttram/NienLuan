from django import forms
import re

import khachhang

from .models import Khach_Hang
from django.core.exceptions import ObjectDoesNotExist
from captcha.fields import ReCaptchaField

class dangkyForm(forms.Form):
    class Meta:
        model = khachhang
        fields = ('username', 'email','matkhau1','matkhau2')
    username = forms.CharField(label='Tài Khoản', max_length='35')
    email = forms.EmailField(label="Gmail")
    matkhau1 = forms.CharField(label='Mật Khẩu' , widget=forms.PasswordInput())
    matkhau2 = forms.CharField(label='Nhập Lại Mật Khẩu' , widget=forms.PasswordInput())
    Captcha = ReCaptchaField()
    #  kiem tra mật khẩu
    def clean_matkhau2(self):
        if 'matkhau1' in self.changed_data:
            matkhau1 = self.cleaned_data['matkhau1']
            matkhau2 = self.cleaned_data['matkhau2']
            # tránh trường hộp matkhau1 các nhiều lần
            if not re.search(r'^[A-Za-z0-9]{5,15}\w+$', matkhau1):
                raise forms.ValidationError("Mật Khẩu Không Hộp Lệ Không Đủ 5-15 Kí Tự.")
            if matkhau1 == matkhau2 and matkhau1:
                return matkhau2
        raise forms.ValidationError("Mật Khẩu Không Giống Nhau.")
   

    
    def clean_username(self):
        username = self.cleaned_data['username']
        if not re.search(r'^[A-Za-z0-9]{5,15}\w+$', username):
            raise forms.ValidationError("Tài Khoản Có Ký Tự Đặt Biệt Hoặc Không Đủ 5-15 Kí Tự.")
        try:
            Khach_Hang.objects.get(username=username)
        except ObjectDoesNotExist:
            return username 
        raise forms.ValidationError("Tài Khoản Đã Tồn tại ")
    
    def save(self):
        Khach_Hang.objects.create_user(username = self.cleaned_data['username'], 
                                email = self.cleaned_data['email'],
                                password = self.cleaned_data['matkhau1']
                                 )
