# Generated by Django 4.0 on 2021-12-22 01:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('khachhang', '0001_initial'),
        ('dathang', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='dat_hang',
            name='khach_hang',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='khachhang.khach_hang'),
        ),
    ]