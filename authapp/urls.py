from django.conf.urls import url

import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    url('login/', authapp.login, name='login'),
    url('logout/', authapp.logout, name='logout'),
    url('register/', authapp.register, name='register'),
    url('edit/', authapp.edit, name='edit'),
]
