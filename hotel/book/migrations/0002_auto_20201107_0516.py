# Generated by Django 3.1.2 on 2020-11-07 05:16

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Booking',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tracking_id', models.CharField(default='000', max_length=64)),
                ('first_name', models.CharField(default=None, max_length=64)),
                ('last_name', models.CharField(default=None, max_length=64)),
                ('email', models.CharField(default=None, max_length=64)),
                ('phone', models.CharField(default=None, max_length=64)),
                ('room', models.IntegerField(default=1)),
                ('adult', models.IntegerField(default=1)),
                ('child', models.IntegerField(default=0)),
                ('checkin_date', models.DateTimeField(default=None)),
                ('checkout_date', models.DateTimeField(default=None)),
                ('booking_date', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.DeleteModel(
            name='Book',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='address',
            new_name='avatar',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='phone_contact',
            new_name='phone',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='latitude',
        ),
        migrations.RemoveField(
            model_name='hotel',
            name='longitude',
        ),
        migrations.AddField(
            model_name='booking',
            name='hotel',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='booking', to='book.hotel'),
        ),
        migrations.AddField(
            model_name='booking',
            name='user',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='booking', to=settings.AUTH_USER_MODEL),
        ),
    ]
