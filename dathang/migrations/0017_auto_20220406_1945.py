# Generated by Django 3.2.10 on 2022-04-06 12:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dathang', '0016_auto_20220406_1940'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dat_hang',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AlterField(
            model_name='dat_hang',
            name='update_at',
            field=models.DateTimeField(auto_now=True, null=True),
        ),
    ]
