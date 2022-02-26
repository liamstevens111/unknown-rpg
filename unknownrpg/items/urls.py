from django.urls import include, path
from .apis import ItemShopListApi, ItemShopBuyApi, ItemShopSellApi

urlpatterns = [
    path('', ItemShopListApi.as_view(), name='shop-list'),
    path('buy/', ItemShopBuyApi.as_view(), name='shop-buy'),
    path('sell/', ItemShopSellApi.as_view(), name='shop-sell'),
]
