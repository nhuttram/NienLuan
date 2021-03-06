# Generated by Django 3.2.10 on 2022-03-16 13:09

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('sanpham', '0013_alter_chi_tiet_san_pham_san_pham'),
    ]

    operations = [
        migrations.CreateModel(
            name='Binh_Luan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('noidung', models.CharField(default='', max_length=255)),
                ('create_at', models.DateTimeField(auto_now_add=True)),
                ('update_at', models.DateTimeField(auto_now=True)),
                ('trang_thai', models.BooleanField(default=True)),
                ('khach_hang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('san_pham', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sanpham.san_pham')),
            ],
        ),
        migrations.DeleteModel(
            name='Ma_Giam_Gia',
        ),
    ]
