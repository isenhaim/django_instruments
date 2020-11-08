from django.contrib.auth.decorators import login_required
from django.shortcuts import render, HttpResponseRedirect
from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm
from django.contrib import auth
from django.urls import reverse
from django.core.mail import send_mail
from django.conf import settings
from authapp.models import ShopUser
from django.db import transaction
from authapp.forms import ShopUserProfileEditForm

# import hashlib
# import urllib
# from django import template
# from django.utils.safestring import mark_safe
#
# register = template.Library()
#
#
# # return only the URL of the gravatar
# # TEMPLATE USE:  {{ email|gravatar_url:150 }}
# @register.filter
# def gravatar_url(email, size=40):
#     default = "https://example.com/static/images/defaultavatar.jpg"
#     return f"https://www.gravatar.com/avatar/{hashlib.md5(email.lower()).hexdigest()}?{urllib.urlencode({'d': default, 's': str(size)})}"
#
#
# # return an image tag with the gravatar
# # TEMPLATE USE:  {{ email|gravatar:150 }}
# @register.filter
# def gravatar(email, size=40):
#     url = gravatar_url(email, size)
#     return mark_safe('<img src="%s" height="%d" width="%d">' % (url, size, size))
#
@login_required
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
        'profile_form': profile_form
    }

    return render(request, 'authapp/edit.html', content)


def verify(request, email, activation_key):
    try:
        user = ShopUser.objects.get(email=email)
        if user.activation_key == activation_key and not user.is_activation_key_expired():
            user.is_active = True
            user.save()
            auth.login(request, user)
            return render(request, 'authapp/verification.html')
        else:
            return render(request, 'authapp/verification.html')
    except Exception as e:
        return HttpResponseRedirect(reverse('main'))


def send_verify_mail(user):
    verify_link = reverse('auth:verify', args=[user.email, user.activation_key])

    title = f'Подтверждение учетной записи {user.username}'

    message = f'Для подтверждения учетной записи {user.username} на портале ' \
              f'{settings.DOMAIN_NAME} перейдите по ссылке: \n{settings.DOMAIN_NAME}{verify_link}'

    return send_mail(title, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def login(request):
    title = 'вход'

    login_form = ShopUserLoginForm(data=request.POST)
    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main'))

    content = {'title': title, 'login_form': login_form}
    return render(request, 'authapp/login.html', content)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('main'))


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            user = register_form.save()

            if send_verify_mail(user):
                return HttpResponseRedirect(reverse('auth:login'))
            else:
                return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()
        content = {'title': title, 'register_form': register_form}
        return render(request, 'authapp/register.html', content)
