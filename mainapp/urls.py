from django.conf.urls import url

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    url(r'^$', mainapp.categories, name='index'),
    url(r'^(?P<cat_id>\d+)/$', mainapp.subCategories, name='category'),
    url(r'^(?P<cat_id>\d+)/(?P<subcat_id>\d+)/$', mainapp.productsOfCategory, name='subcategory'),
    url(r'^(?P<cat_id>\d+)/(?P<subcat_id>\d+)/(?P<product_id>\d+)/$', mainapp.products, name='products'),
]
