import datetime
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from .models import Shop, Product, ProductInShop, Cart, Purchase
from django.contrib.auth.models import User
from app_goods.models import Promotion
from django.core.cache import cache
from django.contrib.auth.mixins import LoginRequiredMixin
from app_users.models import PersonalCabinet
from app_users.forms import ReplenishTheBalanceForm
from django.db.models import Sum, F
from .forms import CartForm
import logging


STATUS_COEFFICIENT = 0.1

logger = logging.getLogger(__name__)


class ShopsListView(generic.ListView):
    model = Shop
    template_name = 'shops/shops_list.html'
    context_object_name = 'shops_list'

    def get_context_data(self, **kwargs):
        context = super(ShopsListView, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated:
            context['user_is_auth'] = True
            user = self.request.user
            context['user'] = user
        return context


class PersonalCabinetView(generic.DetailView):
    model = User
    context_object_name = 'user'
    template_name = 'shops/personal_cabinet.html'

    def get_context_data(self, **kwargs):
        username = self.request.user.username
        context = super(PersonalCabinetView, self).get_context_data(**kwargs)
        promotions_cache_key = 'promotions:{}'.format(username)
        promotions = Promotion.objects.all()
        cache.get_or_set(promotions_cache_key, promotions, 30*60)
        context['promotions'] = promotions
        return context


class ReplenishTheBalanceView(LoginRequiredMixin, generic.View):
    def get(self, request, pk):
        user = User.objects.get(id=pk)
        if self.request.user != user:
            return self.handle_no_permission()
        replenish_balance_form = ReplenishTheBalanceForm()
        return render(request, template_name='shops/replenish_balance.html',
                      context={'replenish_balance_form': replenish_balance_form, 'user_id': pk})

    def post(self, request, pk):
        replenish_balance_form = ReplenishTheBalanceForm(request.POST)
        personal_cabinet = self.request.user.profile.personalcabinet

        if replenish_balance_form.is_valid():
            replenishment = replenish_balance_form.cleaned_data['balance']
            personal_cabinet.balance += replenishment
            personal_cabinet.save(update_fields=['balance'])
            logger.info(
                f'{datetime.datetime.now()} Пользователь {self.request.user.username} '
                f'пополнил баланс на {replenishment}.'
            )
            return redirect(reverse('personal-cabinet', kwargs={'pk': pk}))


class ProductsListView(generic.ListView):
    model = Product
    template_name = 'shops/products_list.html'
    context_object_name = 'products_list'
    # queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        context = super(ProductsListView, self).get_context_data(**kwargs)
        best_selling_product_report = Purchase.objects.values('product').annotate(
            product_quantity=Sum('quantity')).order_by('-product_quantity').first()
        if best_selling_product_report:
            product = Product.objects.get(id=best_selling_product_report['product'])
            best_selling_product_report['name'] = product.name
            best_selling_product_report['id'] = product.id
        shops = []
        for product in Product.objects.prefetch_related('shops'):
            shop_item = [shop.name for shop in product.shops.all()]
            shops.append({
                'id': product.id,
                'name': product.name,
                'shops': shop_item
            })
        context['shops'] = shops
        context['bestseller'] = best_selling_product_report
        return context


class CartView(LoginRequiredMixin, generic.ListView):
    model = Cart
    template_name = 'shops/cart.html'

    def get_context_data(self, **kwargs):
        context = super(CartView, self).get_context_data(**kwargs)
        cart = Cart.objects.filter(user_id=self.request.user.id)
        context['cart_list'] = cart
        context['cart_cost'] = cart.aggregate(total=Sum(F('product__price') * F('quantity')))['total']
        return context

    def post(self, request, *args, **kwargs):
        cart = Cart.objects.filter(user_id=request.user.id)
        user = request.user
        if 'pay' in request.POST:
            total_cost = 0
            for item in cart:
                total_cost += item.total_cost
                item_in_shop = ProductInShop.objects.get(shop=item.shop, product=item.product)
                Purchase.objects.create(
                    user=user,
                    product=item.product,
                    quantity=item.quantity,
                    cost=item.total_cost
                )
                item_in_shop.quantity = F('quantity') - item.quantity
                user.profile.personalcabinet.balance = F('balance') - item.total_cost
                user.profile.personalcabinet.status_points = F('status_points') + item.total_cost * STATUS_COEFFICIENT
                user.profile.personalcabinet.save()
                item_in_shop.save()
                item.delete()
            logger.info(
                f'{datetime.datetime.now()} Покупка от пользователя {user.username} на сумму {total_cost}'
            )
        elif 'refuse' in request.POST:
            for item in cart:
                item.delete()
        return redirect(reverse('shops-list'))


class ShopDetailView(generic.ListView):
    model = ProductInShop
    template_name = 'shops/shop_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ShopDetailView, self).get_context_data(**kwargs)
        context['shop_items'] = ProductInShop.objects.filter(shop_id=self.kwargs['shop_id'])
        context['shop'] = Shop.objects.get(id=self.kwargs['shop_id'])
        return context


class ProductDetailView(generic.DetailView):
    # model = Product
    template_name = 'shops/product_detail.html'

    def get_object(self, queryset=None):
        return Product.objects.get(id=self.kwargs['product_id'])

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data(**kwargs)
        shop_id = self.kwargs['shop_id']
        product_id = self.kwargs['product_id']
        product = ProductInShop.objects.filter(product_id=product_id).get(shop_id=shop_id)
        context['product'] = product
        context['cart_form'] = CartForm
        return context

    def post(self, request, *args, **kwargs):
        cart_object = self.get_object()
        shop = Shop.objects.get(id=kwargs['shop_id'])
        cart_form = CartForm(request.POST)
        if cart_form.is_valid():
            cart = cart_form.save(commit=False)
            cart.user = request.user
            cart.product = cart_object
            cart.shop = shop
            cart.save()
            logger.info(
                f'{datetime.datetime.now()} Пользователь {self.request.user.username} '
                f'добавил продукт ({cart_object.name}) в корзину.'
            )
        return redirect(reverse('cart'))
