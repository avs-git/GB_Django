from django.conf.urls import url

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    url(r'^$', mainapp.categories, name='index'),
    url(r'^(?P<pk>\d+)/$', mainapp.categories, name='categories'),
]
