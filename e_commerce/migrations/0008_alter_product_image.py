# Generated by Django 5.0.6 on 2024-09-09 10:47

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('e_commerce', '0007_alter_product_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=django_resized.forms.ResizedImageField(crop=None, force_format=None, keep_meta=True, null=True, quality=-1, scale=None, size=[100, 100], upload_to='images'),
        ),
    ]
