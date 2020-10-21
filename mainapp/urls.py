from django.urls import path

import mainapp.views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.catalog, name='index'),
    path('<int:pk>/', mainapp.catalog, name='item'),
    path('category/<int:pk>/', mainapp.category, name='category'),
]
