# Generated by Django 3.2.6 on 2021-08-15 05:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('porzotokApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='HotelVisitor',
            fields=[
                ('hotel_visitor_id', models.AutoField(primary_key=True, serialize=False)),
                ('ip_address', models.CharField(max_length=50, unique=True)),
                ('total_view', models.IntegerField()),
                ('date', models.DateField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('hotel_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='porzotokApp.hoteldetails')),
            ],
            options={
                'unique_together': {('hotel_id', 'ip_address')},
            },
        ),
    ]
