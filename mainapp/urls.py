from django.conf.urls import url

import mainapp.views as mainapp

app_name = 'mainapp'

# SETTINGS URLS = products
urlpatterns = [
    url(r'^$', mainapp.categories, name='index'),
    url(r'^category/(?P<cat_id>\d+)/page/(?P<page>\d+)$', mainapp.productsOfCategory, name='category'),
    url(r'^product/(?P<product_id>\d+)/$', mainapp.products, name='products'),
]
