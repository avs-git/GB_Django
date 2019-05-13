from django.conf.urls import url
from django.urls import path

import mainapp.views as mainapp

app_name = 'mainapp'

# SETTINGS URLS = products
urlpatterns = [
    url(r'^$', mainapp.CategoriesList.as_view(), name='index'),
    url(r'^category/(?P<cat_id>\d+)/page/(?P<page>\d+)$', mainapp.ProductsList.as_view(), name='category'),
    path('product/<int:pk>/', mainapp.ProductView.as_view(), name='products'),
]
