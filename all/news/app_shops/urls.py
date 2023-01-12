from django.urls import path
from .views import ShopsListView, PersonalCabinetView, ReplenishTheBalanceView, ProductsListView, CartView, \
    ShopDetailView, ProductDetailView


urlpatterns = [
    path('', ShopsListView.as_view(), name='shops-list'),
    path('personal_cabinet/<int:pk>/', PersonalCabinetView.as_view(), name='personal-cabinet'),
    path('personal_cabinet/<int:pk>/replenish_balance/', ReplenishTheBalanceView.as_view(), name='replenish-balance'),
    path('products/', ProductsListView.as_view(), name='products-list'),
    path('cart/', CartView.as_view(), name='cart'),
    path('<int:shop_id>/', ShopDetailView.as_view(), name='shop-detail'),
    path('<int:shop_id>/product_detail/<int:product_id>/', ProductDetailView.as_view(), name='product-detail')
]
