from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlencode, urlunparse

from django.utils import timezone
from social_core.exceptions import AuthForbidden

from authapp.models import ShopUserProfile
import requests


def save_user_profile(backend, user, response, *args, **kwargs):
    if backend.name != 'google-oauth2':
        return

    if response['picture']:
        img = requests.get(response['picture']).content
        id = response['sub']

        with open(f'media/users_avatars/{id}.jpg', 'wb') as avatar:
            avatar.write(img)

        user.shopuserprofile.avatar = f'users_avatars/{id}.jpg'
        user.save()
