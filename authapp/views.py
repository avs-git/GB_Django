from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from django.db import transaction

from authapp.forms import \
    ShopUserProfileEditForm, \
    ShopUserLoginForm, \
    ShopUserRegisterForm, \
    ShopUserEditForm

from authapp.models import ShopUser

# импортируем главное меню и корзину для отображения на всех страницах
from mainapp.views import common_content


def get_last_referer(request):
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def login(request):
    title = 'вход'

    next = request.META.get('HTTP_REFERER') if 'next' in request.GET.keys() else ''
    login_form = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        print('*' * 50, request.GET.keys())
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                print('*' * 50, next)
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('index'))

    content = {
        **common_content(request),
        'title': title,
        'login_form': login_form,
        'next': next
    }
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()
            if send_verify_mail(user):
                print('сообщение подтверждения отправлено')
                _kwargs = {
                    'status': 1,
                    'email': user.email
                }
                return HttpResponseRedirect(
                    reverse('auth:success_verification_send', kwargs=_kwargs),
                )
            else:
                print('ошибка отправки сообщения')
                _kwargs = {
                    'status': 0,
                }
                return HttpResponseRedirect(
                    reverse('auth:success_verification_send', kwargs=_kwargs),
                )
    else:
        register_form = ShopUserRegisterForm()

    content = {
        **common_content(request),
        'title': title,
        'register_form': register_form,
    }
    return render(request, 'authapp/register.html', content)


def success_verification_send(request, status, email):
    content = {
        'success': status,
        'email': email
    }
    return render(request, 'authapp/verification_send.html', content)


def send_verify_mail(user):
    verify_link = reverse('auth:verify', kwargs={
        'email': user.email,
        'activation_key': user.activation_key,
    })

    title = f'Подтверждение учетной записи {user.username}'
    message = f'Для подтверждения учетной записи {user.username} на портале {settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'
    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key, backend='django.contrib.auth.backends.ModelBackend'):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and user.is_activation_key_valid():
            user.is_active = True
            user.save()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return render(request, 'authapp/verification.html')
        else:
            print(f'error activation user: {user}')
            return render(request, 'authapp/verification.html')
    except Exception as e:
        print(f'error activation user : {e.args}')
        return HttpResponseRedirect(reverse('index'))


@transaction.atomic
def edit(request):
    title = 'редактирование'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(
            instance=request.user.shopuserprofile
        )

    content = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form,
        'user_profile': request.user.shopuserprofile,
    }

    return render(request, 'authapp/edit.html', content)
