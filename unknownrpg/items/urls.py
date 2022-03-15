from django.urls import include, path
from .apis import ItemShopListApi, ItemShopBuyApi, ItemShopSellApi
from characters.apis import CharacterItemsEquipApi, CharacterItemsUnequipApi

urlpatterns = [
    path('shop/', ItemShopListApi.as_view(), name='shop-list'),
    path('buy/', ItemShopBuyApi.as_view(), name='shop-buy'),
    path('sell/', ItemShopSellApi.as_view(), name='shop-sell'),

    path('equip/', CharacterItemsEquipApi.as_view(),
         name='character-items-equip'),
    path('unequip/', CharacterItemsUnequipApi.as_view(),
         name='character-items-unequip'),
]
