# Generated by Django 3.2.10 on 2022-02-05 12:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('sanpham', '0008_alter_chi_tiet_san_pham_san_pham'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chi_tiet_san_pham',
            name='san_pham',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='chitietsanpham1', to='sanpham.san_pham'),
        ),
    ]
