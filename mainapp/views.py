from django.shortcuts import render, get_object_or_404

from mainapp.models import Product, ProductCategory


def main(request):
    content = {}

    return render(request, 'mainapp/index.html', context=content)


def contacts(request):
    content = {}

    return render(request, 'mainapp/contacts.html', context=content)


def catalog(request, pk=None):
    links_menu = ProductCategory.objects.all()

    if pk is not None:
        products = Product.objects.filter(pk=pk)
        content = {
            'products': products,
        }

        return render(request, 'mainapp/lot.html', content)

    products = Product.objects.all()
    title = 'Каталог'
    content = {
        'title': title,
        'links_menu': links_menu,
        'products': products,
    }

    return render(request, 'mainapp/catalog.html', content)


def category(request, pk=None):
    links_menu = ProductCategory.objects.all()
    if pk is not None:
        if pk == 0:
            products = Product.objects.all().order_by('price')
        else:
            products = Product.objects.filter(category__pk=pk)

        content = {
            'links_menu': links_menu,
            'category': category,
            'products': products,
        }

        return render(request, 'mainapp/catalog.html', content)

    same_products = Product.objects.all()

    content = {
        'links_menu': links_menu,
        'products': same_products,
    }

    return render(request, 'mainapp/catalog.html', content)


