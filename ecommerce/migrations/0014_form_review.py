# Generated by Django 5.0.4 on 2024-05-17 05:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0013_remove_product_wishlist_quantity_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='form_review',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('User_id', models.CharField(max_length=255)),
                ('Product_id', models.CharField(max_length=255)),
                ('Review', models.CharField(max_length=255)),
                ('Rating', models.CharField(max_length=255)),
            ],
        ),
    ]
