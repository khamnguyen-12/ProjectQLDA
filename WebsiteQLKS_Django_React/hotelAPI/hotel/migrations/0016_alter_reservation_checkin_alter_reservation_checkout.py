# Generated by Django 5.0.6 on 2024-07-28 05:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('hotel', '0015_alter_bill_totalamount_alter_roomtype_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reservation',
            name='checkin',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='reservation',
            name='checkout',
            field=models.DateTimeField(),
        ),
    ]