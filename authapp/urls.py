from django.conf.urls import url
from django.urls import re_path

import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    url('login/', authapp.login, name='login'),
    url('logout/', authapp.logout, name='logout'),
    re_path(r'^register/$', authapp.register, name='register'),
    url(r'^success_verification_send/(?P<status>\d+)/(?P<email>.+)$', authapp.success_verification_send,
        name='success_verification_send'),
    re_path(r'edit/$', authapp.edit, name='edit'),
    url(r'^verify/(?P<email>.+)/(?P<activation_key>\w+)/$', authapp.verify, name='verify'),
]
