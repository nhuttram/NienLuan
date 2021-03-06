# Generated by Django 3.2.10 on 2022-03-03 04:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sanpham', '0012_auto_20220302_1208'),
        ('giohang', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='san_pham_trong_gio',
            name='gio_hang',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='gio_hang', to='giohang.gio_hang'),
        ),
        migrations.AlterField(
            model_name='san_pham_trong_gio',
            name='san_pham',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='san_pham_gio', to='sanpham.san_pham'),
        ),
    ]
