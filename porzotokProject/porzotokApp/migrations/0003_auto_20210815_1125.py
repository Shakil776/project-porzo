# Generated by Django 3.2.6 on 2021-08-15 05:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('porzotokApp', '0002_hotelvisitor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='hoteldetails',
            name='latitude',
            field=models.CharField(blank=True, default=20.15, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='hoteldetails',
            name='longitude',
            field=models.CharField(blank=True, default=20.15, max_length=50, null=True),
        ),
    ]
