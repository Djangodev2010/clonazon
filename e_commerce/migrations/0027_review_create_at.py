# Generated by Django 5.0.6 on 2024-09-15 06:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('e_commerce', '0026_remove_category_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='create_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
