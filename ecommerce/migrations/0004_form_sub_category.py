# Generated by Django 4.2.7 on 2024-04-09 05:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0003_form_category_image'),
    ]

    operations = [
        migrations.CreateModel(
            name='form_sub_category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Category', models.IntegerField()),
                ('Sub_Category', models.CharField(max_length=255)),
                ('Image', models.ImageField(upload_to='media/')),
            ],
        ),
    ]
