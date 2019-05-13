from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
    # print('back:', backend.name)
    print(response.keys())
    print(response.get('photo'))
    print(response.get('screen_name'))
    print(response.get('user_photo'))

    # VK
    if backend.name == 'vk-oauth2':

        api_url = urlunparse(('https',
                              'api.vk.com',
                              '/method/users.get',
                              None,
                              urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about',)),
                                                    access_token=response['access_token'],
                                                    v='5.92')),
                              None
                              ))

        resp = requests.get(api_url)
        if resp.status_code != 200:
            return

        data = resp.json()['response'][0]
        print(data)
        if data['sex']:
            user.shopuserprofile.gender = ShopUserProfile.MALE if data['sex'] == 2 else ShopUserProfile.FEMALE

        if data['about']:
            user.shopuserprofile.aboutMe = data['about']

        if data['id']:
            user.shopuserprofile.vk_link = 'https://vk.com/id' + str(data['id'])

        if response.get('photo'):
            user.shopuserprofile.vk_photo = response.get('photo')

        if data['bdate']:
            bdate = datetime.strptime(data['bdate'], '%d.%m.%Y').date()

            age = timezone.now().date().year - bdate.year
            if age < 18:
                user.delete()
                raise AuthForbidden('social_core.backends.vk.VKOAuth2')

    # GOOGLE PLUS
    if backend.name == "google-oauth2":
        print('google-oauth2')
        if 'gender' in response.keys():
            if response['gender'] == 'male':
                user.shopuserprofile.gender = ShopUserProfile.MALE
            else:
                user.shopuserprofile.gender = ShopUserProfile.FEMALE

        if 'tagline' in response.keys():
            user.shopuserprofile.tagline = response['tagline']

        if 'aboutMe' in response.keys():
            user.shopuserprofile.aboutMe = response['aboutMe']

        # не работает, так как g+ не отдаёт ageRange
        if 'ageRange' in response.keys():
            minAge = response['ageRange']['min']
            if int(minAge) < 100:
                user.delete()
                raise AuthForbidden('social_core.backends.google.GoogleOAuth2')

        if 'locale' in response.keys():
            user.shopuserprofile.locale = response['locale']

    user.save()
