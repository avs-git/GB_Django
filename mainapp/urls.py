from django.conf.urls import url

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    url(r'^$', mainapp.categories, name='index'),
    url(r'^category/(?P<cat_id>\d+)/$', mainapp.subCategories, name='category'),
    url(r'^category/(?P<cat_id>\d+)/(?P<scat_id>\d+)/$', mainapp.productsOfCategory, name='subcategory'),
    url(r'^product/(?P<product_id>\d+)/$', mainapp.products, name='products'),
]
