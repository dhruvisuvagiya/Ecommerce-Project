# Generated by Django 5.0.4 on 2024-04-15 05:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ecommerce', '0006_reg_login'),
    ]

    operations = [
        migrations.CreateModel(
            name='cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Image', models.ImageField(upload_to='media/')),
                ('Title', models.CharField(max_length=255)),
                ('Price', models.IntegerField()),
                ('Quantity', models.IntegerField()),
                ('Total', models.CharField(max_length=255)),
            ],
        ),
    ]
