# Generated by Django 3.2.10 on 2022-04-06 12:49

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dathang', '0018_auto_20220406_1948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='dat_hang',
            name='create_at',
            field=models.DateTimeField(blank=True, default=datetime.date.today, null=True),
        ),
        migrations.AlterField(
            model_name='dat_hang',
            name='update_at',
            field=models.DateTimeField(blank=True, default=datetime.date.today, null=True),
        ),
    ]