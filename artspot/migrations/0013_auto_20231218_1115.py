# Generated by Django 3.2.23 on 2023-12-18 11:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('artspot', '0012_auto_20231218_0949'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='category',
            options={'verbose_name_plural': 'categories'},
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='media'),
        ),
    ]