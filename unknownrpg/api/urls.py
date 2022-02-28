from django.urls import include, path
from authentication.apis import TestApi

urlpatterns = [
    path('auth/', include('authentication.urls')),
    path('users/', include('users.urls')),
    path('shop/', include('items.urls')),
    path('characters/', include('characters.urls')),

    path('test/', TestApi.as_view()),
]
