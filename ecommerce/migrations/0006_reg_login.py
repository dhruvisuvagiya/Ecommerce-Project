# Generated by Django 4.2.7 on 2024-04-13 10:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0005_form_add_product'),
    ]

    operations = [
        migrations.CreateModel(
            name='reg_login',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Name', models.CharField(max_length=255)),
                ('Email', models.EmailField(max_length=255)),
                ('Password', models.CharField(max_length=255)),
            ],
        ),
    ]
