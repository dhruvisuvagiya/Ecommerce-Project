from django.db import models
from django.forms import ModelForm

# Create your models here.

class reg(models.Model):
    Name=models.CharField(max_length=255)
    Email=models.EmailField(max_length=255)
    Password=models.CharField(max_length=255)
    
class form_category(models.Model):
    Category=models.CharField(max_length=255)
    Image=models.ImageField(upload_to='media/')
    
class categorydata(ModelForm):
    class Meta:
        model = form_category
        fields = ['Category','Image']
        
class form_sub_category(models.Model):
    Category=models.IntegerField()
    Sub_Category=models.CharField(max_length=255)
    Image=models.ImageField(upload_to='media/')
    
class subcategorydata(ModelForm):
    class Meta:
        model = form_sub_category
        fields = ['Category','Sub_Category','Image']

class form_add_product(models.Model):
    Category=models.IntegerField()
    Sub_Category=models.IntegerField()
    Image=models.ImageField(upload_to='media/')
    Title=models.CharField(max_length=255)
    Description=models.CharField(max_length=255)
    Quantity=models.IntegerField()
    Price=models.IntegerField()
    
class addproductdata(ModelForm):
    class Meta:
        model = form_add_product
        fields = ['Category','Sub_Category','Image','Title','Description','Quantity','Price']

class reg_login(models.Model):
    Name=models.CharField(max_length=255)
    Email=models.EmailField(max_length=255)
    Password=models.CharField(max_length=255)

class product_cart(models.Model):
    User_id=models.CharField(max_length=255)
    Image=models.CharField(max_length=255)
    Title=models.CharField(max_length=255)
    Price=models.IntegerField()
    Quantity=models.IntegerField()
    Total=models.CharField(max_length=255)

class product_wishlist(models.Model):
    User_id=models.CharField(max_length=255)
    Image=models.CharField(max_length=255)
    Title=models.CharField(max_length=255)
    Price=models.IntegerField()
    Stock=models.CharField(max_length=255)

class form_review(models.Model):
    User_id=models.CharField(max_length=255)
    Product_id=models.CharField(max_length=255)
    Review=models.CharField(max_length=255)
    Rating=models.CharField(max_length=255)



