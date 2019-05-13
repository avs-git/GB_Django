from django.conf.urls import url

import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    url('login/', authapp.login, name='login'),
    url('logout/', authapp.logout, name='logout'),
    url('register/', authapp.register, name='register'),
    url(r'^success_verification_send/(?P<status>\d+)/(?P<email>.+)$', authapp.success_verification_send,
        name='success_verification_send'),
    url('edit/', authapp.edit, name='edit'),
    url(r'^verify/(?P<email>.+)/(?P<activation_key>\w+)/$', authapp.verify, name='verify'),
]
