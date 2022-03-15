from django.urls import include, path
from .apis import CharacterListApi, CharacterDetailApi, CharacterItemsListApi

urlpatterns = [
    path('', CharacterListApi.as_view(), name='character-list'),
    path('<str:name>/', CharacterDetailApi.as_view(), name='character-detail'),
    path('<str:name>/items/', CharacterItemsListApi.as_view(),
         name='character-items-list'),
]
