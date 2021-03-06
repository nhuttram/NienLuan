# Generated by Django 4.0 on 2021-12-22 01:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('sanpham', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gio_Hang',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_at', models.DateField(auto_now_add=True)),
                ('update_at', models.DateField(auto_now=True)),
            ],
        ),
        migrations.CreateModel(
            name='San_Pham_Trong_Gio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('so_luong', models.IntegerField(default=0)),
                ('gio_hang', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='giohang.gio_hang')),
                ('san_pham', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sanpham.san_pham')),
            ],
        ),
    ]
