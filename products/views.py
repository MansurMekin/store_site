from django.contrib.auth.decorators import login_required
from django.shortcuts import HttpResponseRedirect
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.core.cache import cache

from common.views import TitleMixin
from products.models import Basket, Product, ProductCategory

# Функция = контроллеры = вьюхи


class IndexView(TitleMixin, TemplateView):
    template_name = 'products/index.html'
    title = 'Store'


class ProductListView(TitleMixin, ListView):
    model = Product
    template_name = 'products/products.html'
    title = 'Store - Каталог'
    paginate_by = 3

    def get_queryset(self):
        query_set = super(ProductListView, self).get_queryset()
        category_id = self.kwargs.get('category_id')
        return query_set.filter(category_id=category_id) if category_id else query_set

    def get_context_data(self, **kwargs):
        context = super(ProductListView, self).get_context_data()
        categories = cache.get('categories')
        if not categories:
            context['categories'] = ProductCategory.objects.all()
            cache.set('categories', context['categories'], 30)
        else:
            context['categories'] = categories
        return context


@login_required
def basket_add(request, product_id):
    product = Product.objects.get(id=product_id)
    baskets = Basket.objects.filter(user=request.user, product=product)

    if not baskets.exists():
        Basket.objects.create(user=request.user, product=product, quantity=1)
    else:
        basket = baskets.first()
        basket.quantity += 1
        basket.save()

    return HttpResponseRedirect(request.META['HTTP_REFERER'])


@login_required
def basket_remove(request, basket_id):
    basket = Basket.objects.get(id=basket_id)
    basket.delete()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])


# def products(request, category_id=None, page_number=1):
#     products = Product.objects.filter(
#         category_id=category_id) if category_id else Product.objects.all()
#     per_page = 3
#     paginator = Paginator(products, per_page=per_page)
#     products_paginator = paginator.page(page_number)
#     context = {
#         'title': 'Store - Каталог',
#         'categories': ProductCategory.objects.all(),
#         'products': products_paginator,
#     }
#     return render(request, 'products/products.html', context)


# НЕ нужен так CBV так как мы копируем тот же FBV
# class BasketCreateView(CreateView):
#     model = Basket

#     def post(self, request, *args, **kwargs):
#         product = Product.objects.get(id=self.kwargs.get('product_id'))
#         baskets = Basket.objects.filter(user=request.user, product=product)


# def index(request):
#     context = {
#         'title': 'Store',
#     }
#     return render(request, 'products/index.html', context)
