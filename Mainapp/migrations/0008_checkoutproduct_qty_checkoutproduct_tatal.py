# Generated by Django 4.1.7 on 2023-10-23 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Mainapp', '0007_checkout_shipping'),
    ]

    operations = [
        migrations.AddField(
            model_name='checkoutproduct',
            name='qty',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='checkoutproduct',
            name='tatal',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]