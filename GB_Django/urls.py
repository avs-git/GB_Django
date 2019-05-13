"""GB_Django URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from django.contrib import admin
from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
import mainapp.views as mainapp

urlpatterns = [
    url(r'^$', mainapp.main, name='index'),
    url(r'^catalog/', include('mainapp.urls', namespace='products')),
    url(r'^contacts/', mainapp.contacts, name='contacts'),
    url('auth/', include('authapp.urls', namespace='auth')),
    # url(r'^auth/verify/', include("social_django.urls", namespace="social")),
    url('basket/', include('basketapp.urls', namespace='basket')),
    url('admin/', include('adminapp.urls', namespace='myadmin')),
    url('^social/', include('social_django.urls', namespace='social')),
    url('^orders/', include('ordersapp.urls', namespace='orders')),
    url('admin_old/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns.append(url('__debug__/', include(debug_toolbar.urls)))
