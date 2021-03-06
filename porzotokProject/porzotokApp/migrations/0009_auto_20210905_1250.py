# Generated by Django 3.1.7 on 2021-09-05 06:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('porzotokApp', '0008_auto_20210904_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='block_status',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False),
        ),
        migrations.CreateModel(
            name='OTPmodels',
            fields=[
                ('otp_id', models.AutoField(primary_key=True, serialize=False)),
                ('otp_key', models.CharField(default='K7635OURNMWZ4BFGBBGFK2TFWEAC44YV', max_length=255, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='otp', to='porzotokApp.user')),
            ],
        ),
    ]
