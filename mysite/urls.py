"""
URL configuration for mysite project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.conf import settings
from django.conf.urls.static import static
from ecommerce import views



from django.contrib import admin
from django.urls import path
from ecommerce.views import index_1,admin_index,login,logout,register,register_login,login_cart,logout_cart
from ecommerce.views import category_list,category_list1,product,about,blog,elements_products,review,cart,edit_product,del_product
from ecommerce.views import intro_slider
from ecommerce.views import category,data_category,edit_category,del_category
from ecommerce.views import sub_category,data_sub_category,edit_sub_category,del_sub_category
from ecommerce.views import add_product,data_add_product,edit_add_product,del_add_product
from ecommerce.views import wishlist,del_wishlist,getdata
from ecommerce.views import furniture,electronic,fashion,shoes,market,games,book,sport,tools

urlpatterns = [
    path('', index_1),
    path('admin/', admin_index),
    path('login/', login),
    path('logout/', logout),
    path('register/', register),
    path('reg-cart/', register_login),
    path('login-cart/', login_cart),
    path('logout-cart/', logout_cart),
    path('getdata/', getdata),
    
    path('category-list/', category_list),
    path('category-list1/', category_list1),
    path('product/<id>', product),
    path('about/', about),
    path('blog/', blog),
    path('elements-products/', elements_products),
    path('review/<id>', review),
    # path('cart/', cart),
    path('edit-product/<id>', edit_product),
    path('del-product/<id>', del_product),
    
    path('intro-slider/', intro_slider),
    
    path('category/', category),
    path('data-category/', data_category),
    path('edit-category/<id>', edit_category),
    path('del-category/<id>', del_category),
    
    path('sub-category/', sub_category),
    path('data-sub-category/', data_sub_category),
    path('edit-sub-category/<id>', edit_sub_category),
    path('del-sub-category/<id>', del_sub_category),
    
    path('add-product/', add_product),
    path('data-add-product/', data_add_product),
    path('edit-add-product/<id>', edit_add_product),
    path('del-add-product/<id>', del_add_product),

    path('wishlist/', wishlist),
    path('del-wishlist/<id>', del_wishlist),
    path('cart/', views.cart, name='cart'),
    # path('wishlist/', views.wishlist, name='wishlist'),

    path('Furniture/<id>', furniture),
    path('Electronic/<id>', electronic),
    path('Fashion/<id>', fashion),
    path('Shoes/<id>', shoes),
    path('Market/<id>', market),
    path('Games/<id>', games),
    path('Book/<id>', book),
    path('Sport/<id>', sport),
    path('Tools/<id>', tools),
    
    path('admin/', admin.site.urls),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
