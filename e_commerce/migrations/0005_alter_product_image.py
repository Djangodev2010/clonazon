# Generated by Django 5.0.6 on 2024-09-08 14:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_commerce', '0004_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(upload_to='media/images/'),
        ),
    ]
