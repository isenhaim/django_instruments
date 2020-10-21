from django import template
from django.conf import settings

register = template.Library()


@register.filter(name='media_products')
def media_products(string):
    if not string:
        string = 'products_images/default.jpg'

    return f'{settings.MEDIA_URL}{string}'


@register.filter(name='media_users')
def media_users(string):
    if not string:
        string = 'users_avatars/default.jpg'

    return f'{settings.MEDIA_URL}{string}'


register.filter('media_products', media_products)
register.filter('media_users', media_users)
