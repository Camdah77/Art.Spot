# Generated by Django 3.2.23 on 2023-12-18 13:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artspot', '0013_auto_20231218_1115'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='product_images'),
        ),
    ]
