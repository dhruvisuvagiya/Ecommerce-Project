from django.shortcuts import render
from django.shortcuts import redirect
from django.http import HttpResponse
from django.http import JsonResponse
from django.core.paginator import Paginator

# Create your views here.

from ecommerce.models import reg
from ecommerce.models import reg_login

from ecommerce.models import product_cart
from ecommerce.models import product_wishlist

from ecommerce.models import form_category
from ecommerce.models import categorydata

from ecommerce.models import form_sub_category
from ecommerce.models import subcategorydata

from ecommerce.models import form_add_product
from ecommerce.models import addproductdata

from ecommerce.models import form_review

def index_1(req):
    
    data = form_category.objects.all().values()
    data1 = form_add_product.objects.all().values()
    # data1 = form_add_product.objects.all().values_list()
    data4 = form_add_product.objects.all().values().order_by('-id')[:5][::-1]
    
    if 'name' in req.session:
        id=req.session['name']
        data2 = product_cart.objects.filter(User_id=id).values()
        cart = data2.count()
    else:
        data2 = None
        cart = 0
        id = 'Not Logined'

    if 'name' in req.session:
        data3 = product_wishlist.objects.filter(User_id=id).values()
        wish = data3.count()
    else:
        data3 = None
        wish = 0

    if 'search' in req.GET:
        query = req.GET['search']
        results = form_add_product.objects.filter(Title__icontains=query)

        return render(req,'category-list.html',{'results':results,'data':data})

    return render(req,'index-1.html',{'data':data,'data1':data1,'data2':data2,'data3':data3,'id':id,'cart':cart,'wish':wish,'data4':data4})

def admin_index(req):

    if 'id' not in req.session:
        return redirect('/login/')
    
    id = req.session['id']

    name = ''

    if id:
        data = reg.objects.filter(id=id).values()
        for x in data:
            name = x['Name']

    return render(req,'admin.html',{'id':name})

def login(req):
    
    if req.method=="POST":
        username=req.POST['nm']
        password=req.POST['ps']
        
        data=reg.objects.filter(Name=username,Password=password)
        
        if data.count()==1:
            info = data.get()
            req.session['id'] = info.id
            return redirect('/admin/')
        else:
            return redirect('/login/')
    
    return render(req,'login.html')

def logout(req):
    del req.session['id']
    return redirect('/login/')

def register(req):

    if req.method=="POST":
        
        name=req.POST['nm']
        email=req.POST['em']
        password=req.POST['ps']
        rpassword=req.POST['rps']
        
        if name!='' and email!='' and password!='' and rpassword!='':
            
            if password!=rpassword:
                return redirect('/register')
            else:
                r=reg(
                    Name=name,
                    Email=email,
                    Password=password
                )
            
                r.save()
                return redirect('/login')
        else:
            return redirect('/register')
    
    return render(req,'register.html')

def about(req):

    data = form_category.objects.all().values()

    return render(req,'about.html',{'data':data})

def blog(req):

    data = form_category.objects.all().values()

    return render(req,'blog.html',{'data':data})

def category_list(req):

    data = form_category.objects.all().values()
    
    return render(req,'category-list.html',{'data':data})

def category_list1(req):

    data0 = form_category.objects.all().values()
    data = form_add_product.objects.all().values()
    data1 = form_sub_category.objects.all().values()

    if req.method=='POST':
        check = req.POST.getlist('check[]')
        print('check = ',check)

        for x in check:
            print(x)
            
            if x != '':
                data = form_add_product.objects.filter(Sub_Category__in=check).values()
                # data = form_add_product.objects.filter(Sub_Category__in=[val,val]).values()
            else:
                data = form_add_product.objects.all().values()

    if req.method=='POST' and req.POST.get('action') == 'price':
        price = req.POST.get('pr')
        print('price = ',price)

        if price != '':
            data = form_add_product.objects.filter(Price__range=('0',price)).values()
            # data = form_add_product.objects.filter(Price__range=('','')).values()
            print(data)
        else:
            data = form_add_product.objects.all().values()
    
    return render(req,'category-list1.html',{'data':data,'data1':data1,'data0':data0})

def getdata(req):

    # if req.method=='POST':

    check = req.POST['check[]']
    data = form_add_product.objects.filter(Sub_Category=check).values()
    # print(data)

    for x in data:
        img = x['Image']
        title = x['Title']
        des = x['Description']
        # arr.append(
        #     {'image':image,
        #      'title':title,
        #      'des':des}
        #     )
        # print(arr)

    return JsonResponse({'img':img,'title':title,'des':des})

def elements_products(req):

    data = form_category.objects.all().values()
    
    return render(req,'elements-products.html',{'data':data})

def review(req,id):

    data = form_category.objects.all().values()
    data1 = form_add_product.objects.filter(id=id).values()
    for x in data1:
        pid = x['id']
        img = x['Image']

    if req.method=='POST' and 'name' in req.session:
        msg=req.POST['msg']
        if msg != '':
            msg = req.POST['msg']
        else:
            msg = '-'
        user = req.session['name']
        rating = req.POST['btn']

        r = form_review(
            User_id=user,
            Product_id=pid,
            Review=msg,
            Rating=rating
        )
        r.save()
        return redirect('/product/' + id)
    elif 'name' not in req.session:
        return redirect('/login-cart/')
       
    return render(req,'review.html',{'data':data,'img':img})

def product(req, id):
    data2 = form_category.objects.all().values()
    data = form_add_product.objects.filter(id=id).values()
    for x in data:
        id = x['id']
    data1 = form_add_product.objects.get(id=id)

    x=''

    if 'name' in req.session and req.method == 'POST' and req.POST.get('action') == 'cart':
        img = data1.Image
        title = data1.Title
        price = data1.Price
        qty = req.POST['qtyy']

        if qty != '':
            user = req.session['name']
            total = int(price) * int(qty)

            p = product_cart(
                Image=img,
                Title=title,
                Price=price,
                Quantity=qty,
                Total=total,
                User_id=user
            )
            p.save()
            return redirect('cart')
        else:
            x = 'Select Quantity...!'

    elif 'name' in req.session and req.method == 'POST' and req.POST.get('action') == 'wishlist':
        img = data1.Image
        title = data1.Title
        price = data1.Price
        qty = data1.Quantity
        if qty > 0:
            stock = 'In Stock'
        elif qty <= 0:
            stock = 'Out of Stock'
        user = req.session['name']

        p = product_wishlist(
            Image=img,
            Title=title,
            Price=price,
            User_id=user,
            Stock=stock
        )
        p.save()
        return redirect('/wishlist/')
    
    data3 = form_review.objects.filter(Product_id=id).values()

    return render(req, 'product.html', {'data': data,'x':x,'data2':data2,'id':id,'data3':data3})

# def product(req,id):

#     data = form_add_product.objects.filter(id=id).values()
#     data1=form_add_product.objects.get(id=id)

#     # for x in data:
#     #     x['Image']
#     #     x['Title']
#     #     x['Price']

#     if wishlist:
#         if 'name' in req.session:
#             img=data1.Image
#             title=data1.Title
#             price=data1.Price
#             qty=data1.Quantity
#             if qty > 0:
#                 stock='In Stock'
#             elif qty <= 0:
#                 stock='Out of Stock'
#             user=req.session['name']

#             p=product_wishlist(
#                 Image=img,
#                 Title=title,
#                 Price=price,
#                 User_id=user,
#                 Stock=stock
#             )
#             p.save()
#             return redirect('/wishlist/')
#     if cart:
#         if 'name' in req.session:
#             if req.method=='POST':
#                 img=data1.Image
#                 title=data1.Title
#                 price=data1.Price
#                 qty=req.POST['qtyy']
#                 user=req.session['name']
#                 total=int(price)*int(qty)

#                 p=product_cart(
#                     Image=img,
#                     Title=title,
#                     Price=price,
#                     Quantity=qty,
#                     Total=total,
#                     User_id=user
#                 )
#                 p.save()
#                 return redirect('/cart/')
#         else:
#             return render(req,'product.html',{'data':data})

#     return render(req,'product.html',{'data':data})

def cart(req):

    if 'name' not in req.session:
        return redirect('/login-cart/')

    id=req.session['name']

    data1 = form_category.objects.all().values()
    data = product_cart.objects.filter(User_id=id).values()

    total=0

    for x in data:
        total+=int(x['Total'])

    if 'search' in  req.POST:
        search = req.POST["search"]
        data  = product_cart.objects.filter(Title__icontains=search,User_id=id)

    return render(req,'cart.html',{'data':data,'total':total,'data1':data1})

def edit_product(req,id):

    data1 = product_cart.objects.filter(id=id).get()
    data = product_cart.objects.filter(id=id).values()
    for x in data:
        price=x['Price']

    if req.method=='POST':
        qty=req.POST['qtyy']
        total=int(price)*int(qty)

        data1.Quantity=qty
        data1.Total=total

        data1.save()
        return redirect('/cart/')
    
    return render(req,'product.html',{'data1':data1,'data':data})

def del_product(req,id):
    
    product_cart.objects.filter(id=id).delete()    
    
    return redirect('/cart/')

def wishlist(req):

    if 'name' not in req.session:
        return redirect('/login-cart/')

    id=req.session['name']

    data1 = form_category.objects.all().values()
    data = product_wishlist.objects.filter(User_id=id).values()

    for x in data:
        title = x['Title']

    data2 = form_add_product.objects.filter(Title=title).values()
    for x in data2:
        id = x['id']

    if 'search' in  req.GET:
        search = req.GET["search"]
        data  = product_wishlist.objects.filter(Title__icontains=search,User_id=id)

    return render(req,'wishlist.html',{'data':data,'id':id,'data1':data1})

def del_wishlist(req,id):
    
    product_wishlist.objects.filter(id=id).delete()    
    
    return redirect('/wishlist/')

def intro_slider(req):
    
    id = req.session['id']

    name = ''

    if id:
        data = reg.objects.filter(id=id).values()
        for x in data:
            name = x['Name']
    
    return render(req,'intro-slider.html',{'id':name})

def basic_table(req):
    
    id = req.session['id']

    name = ''

    if id:
        data = reg.objects.filter(id=id).values()
        for x in data:
            name = x['Name']

    return render(req,'basic-table.html',{'id':name})

def category(req):
    
    id = req.session['id']

    name = ''

    if id:
        data = reg.objects.filter(id=id).values()
        for x in data:
            name = x['Name']
            
    frm=categorydata()
    
    if req.method=='POST':
        frm=categorydata(req.POST,req.FILES)
        frm.save()
        return redirect('/admin/')
    
    return render(req,'category.html',{'id':name,'frm':frm})

def data_category(req):
    
    id = req.session['id']

    name = ''

    if id:
        data = reg.objects.filter(id=id).values()
        for x in data:
            name = x['Name']
    
    data=form_category.objects.all().values()
    
    return render(req,'data-category.html',{'id':name,'data':data})

def edit_category(req,id):

    data=form_category.objects.get(id=id)
    form = categorydata(instance=data)
    
    if req.method=="POST":
        
        form = categorydata(req.POST,req.FILES,instance=data)
        form.save(commit=True)
        return redirect('/data-category/')
        
        # if form.is_valid():
        # doc = form.save(commit=True)
        # doc = form.save(commit=False)
        # doc.save()
    
    return render(req,'category.html',{'data':data,'frm':form})

def del_category(req,id):
    
    form_category.objects.filter(id=id).delete()    
    
    return redirect('/data-category/')

def sub_category(req):
    
    id = req.session['id']

    name = ''

    if id:
        data = reg.objects.filter(id=id).values()
        for x in data:
            name = x['Name']
            
    data = form_category.objects.all().values()
    
    frm=subcategorydata()
    
    if req.method=='POST':
        frm=subcategorydata(req.POST,req.FILES)
        frm.save()
        return redirect('/data-sub-category/')
    
    return render(req,'sub-category.html',{'id':name,'data':data,'frm':frm})

def data_sub_category(req):
    
    id = req.session['id']

    name = ''

    if id:
        data = reg.objects.filter(id=id).values()
        for x in data:
            name = x['Name']
    
    data=form_sub_category.objects.all().values()
    
    return render(req,'data-sub-category.html',{'id':name,'data':data})

def edit_sub_category(req,id):
    
    data=form_sub_category.objects.get(id=id)
    frm = subcategorydata(instance=data)
    
    if req.method=="POST":
        
        frm = subcategorydata(req.POST,req.FILES,instance=data)
        frm.save(commit=True)
        return redirect('/data-sub-category/')
    
    return render(req,'sub-category.html',{'frm':frm})

def del_sub_category(req,id):
    
    form_sub_category.objects.filter(id=id).delete()    
    
    return redirect('/data-sub-category/')

def add_product(req):
    
    id = req.session['id']

    name = ''

    if id:
        data = reg.objects.filter(id=id).values()
        for x in data:
            name = x['Name']
            
    data = form_category.objects.all().values()
    data1 = form_sub_category.objects.all().values()
    
    frm=addproductdata()
    
    if req.method=='POST':
        frm=addproductdata(req.POST,req.FILES)
        frm.save()
        return redirect('/data-add-product/')
    
    return render(req,'add-product.html',{'id':name,'data':data,'data1':data1,'frm':frm})

def data_add_product(req):
    
    id = req.session['id']

    name = ''

    if id:
        data = reg.objects.filter(id=id).values()
        for x in data:
            name = x['Name']
    
    data=form_add_product.objects.all().values()
    
    return render(req,'data-add-product.html',{'id':name,'data':data})

def edit_add_product(req,id):
    
    data=form_add_product.objects.get(id=id)
    frm = addproductdata(instance=data)
    
    if req.method=="POST":
        
        frm = addproductdata(req.POST,req.FILES,instance=data)
        frm.save(commit=True)
        return redirect('/data-add-product/')
    
    return render(req,'add-product.html',{'frm':frm})

def del_add_product(req,id):
    
    form_add_product.objects.filter(id=id).delete()    
    
    return redirect('/data-add-product/')

def register_login(req):

    x='';y='';z=''

    if req.method=="POST":
        
        name=req.POST['nm']
        email=req.POST['em']
        password=req.POST['ps']
        
        if name=='':
            x = 'Please Enter Your Name...!' 
        elif email=='':
            y = 'Please Enter Email Id...!' 
        elif password=='':
            z = 'Please Enter Password...!'
            # return redirect('/reg-cart/')
        else:
            r=reg_login(
                Name=name,
                Email=email,
                Password=password
            )
            
            r.save()
            return redirect('/login-cart/')
    
    return render(req,'register-index.html',{'x':x,'y':y,'z':z})  

def login_cart(req):

    if req.method=="POST":
        username=req.POST['nm']
        password=req.POST['ps']
        
        data=reg_login.objects.filter(Name=username,Password=password)

        if data.count()==1:
            info = data.get()
            req.session['name'] = info.Name
            return redirect('/')
        else:
            return redirect('/login-cart/')
    
    return render(req,'login-index.html')  

def logout_cart(req):
    if 'name' not in req.session:
        return HttpResponse('You are already logout')
    del req.session['name']
    return redirect('/login-cart/')

def furniture(req,id):

    category = ''

    data = form_add_product.objects.filter(Category=id).values()
    for x in data:
        cat = x['Category']
        data1 = form_category.objects.filter(id=cat).values()
        for x in data1:
            category = x['Category']

    return render(req,'category-product.html',{'data':data,'cat':category})

def electronic(req,id):

    category = ''

    data = form_add_product.objects.filter(Category=id).values()

    for x in data:
        cat = x['Category']
        data1 = form_category.objects.filter(id=cat).values()
        for x in data1:
            category = x['Category']

    return render(req,'category-product.html',{'data':data,'cat':category})

def fashion(req,id):

    category = ''

    data = form_add_product.objects.filter(Category=id).values()
    for x in data:
        cat = x['Category']
        data1 = form_category.objects.filter(id=cat).values()
        for x in data1:
            category = x['Category']

    return render(req,'category-product.html',{'data':data,'cat':category})

def shoes(req,id):
    
    category = ''
    
    data = form_add_product.objects.filter(Category=id).values()
    for x in data:
        cat = x['Category']
        data1 = form_category.objects.filter(id=cat).values()
        for x in data1:
            category = x['Category']
    return render(req,'category-product.html',{'data':data,'cat':category})

def market(req,id):

    category = ''

    data = form_add_product.objects.filter(Category=id).values()
    for x in data:
        cat = x['Category']
        data1 = form_category.objects.filter(id=cat).values()
        for x in data1:
            category = x['Category']

    return render(req,'category-product.html',{'data':data,'cat':category})

def games(req,id):

    category = ''
    
    data = form_add_product.objects.filter(Category=id).values()
    for x in data:
        cat = x['Category']
        data1 = form_category.objects.filter(id=cat).values()
        for x in data1:
            category = x['Category']

    return render(req,'category-product.html',{'data':data,'cat':category})

def book(req,id):

    category = ''
    
    data = form_add_product.objects.filter(Category=id).values()
    for x in data:
        cat = x['Category']
        data1 = form_category.objects.filter(id=cat).values()
        for x in data1:
            category = x['Category']

    return render(req,'category-product.html',{'data':data,'cat':category})

def sport(req,id):

    category = ''
    
    data = form_add_product.objects.filter(Category=id).values()
    for x in data:
        cat = x['Category']
        data1 = form_category.objects.filter(id=cat).values()
        for x in data1:
            category = x['Category']

    return render(req,'category-product.html',{'data':data,'cat':category})

def tools(req,id):

    category = ''
    
    data = form_add_product.objects.filter(Category=id).values()
    for x in data:
        cat = x['Category']
        data1 = form_category.objects.filter(id=cat).values()
        for x in data1:
            category = x['Category']
    
    return render(req,'category-product.html',{'data':data,'cat':category})

