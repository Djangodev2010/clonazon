# Generated by Django 5.0.6 on 2024-09-17 05:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_commerce', '0031_alter_profile_cart'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='rating',
            field=models.IntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10'), (11, '11'), (12, '12'), (13, '13'), (14, '14'), (15, '15'), (16, '16'), (17, '17'), (18, '18'), (19, '19'), (20, '20')], default=1),
        ),
    ]
