# Generated by Django 3.1.3 on 2020-12-11 12:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0008_booking_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='booking',
            name='price',
            field=models.CharField(default=None, max_length=64, null=True),
        ),
    ]
