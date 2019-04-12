from django.urls import path

import basketapp.views as basketapp

app_name = 'basketapp'

urlpatterns = [
    path('', basketapp.basket, name='view'),
    path('add/<int:pk>/', basketapp.basket_add, name='add'),
    path('remove/<int:pk>)/', basketapp.basket_remove, name='remove'),
    path('remove_item/<int:pk>)/', basketapp.basket_remove_item, name='remove_item'),
    path('edit/<int:pk>/<int:quantity>/', basketapp.basket_edit, name='edit'),
    path('drop/', basketapp.basket_drop, name='drop'),
]
