from django.shortcuts import render, get_object_or_404
from django.conf import settings
from django.views.decorators.cache import cache_page
from django.core.cache import cache
from mainapp.models import Product, ProductCategory


def main(request):
    content = {}

    return render(request, 'mainapp/index.html', context=content)


def contacts(request):
    content = {}

    return render(request, 'mainapp/contacts.html', context=content)


@cache_page(3600)
def catalog(request, pk=None):
    links_menu = get_links_menu()

    if pk is not None:
        products = get_products()
        content = {
            'products': products,
        }

        return render(request, 'mainapp/lot.html', content)

    products = get_products()
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


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter()
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__is_active=True).select_related('category')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        product = cache.get(key)
        if product is None:
            product = get_object_or_404(Product, pk=pk)
            cache.set(key, product)
        return product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_orederd_by_price():
    if settings.LOW_CACHE:
        key = 'products_orederd_by_price'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).order_by('price')


def get_products_in_category_orederd_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_orederd_by_price_{pk}'
        products = cache.get(key)
        if products is None:
            products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by(
                'price')
            cache.set(key, products)
        return products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).order_by('price')
