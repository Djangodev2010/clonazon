# Generated by Django 5.0.6 on 2024-09-17 05:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_commerce', '0030_review_stars_alter_cartitem_quantity'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='cart',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='e_commerce.cartitem'),
        ),
    ]
