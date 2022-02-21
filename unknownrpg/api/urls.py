from django.urls import include, path
from authentication.apis import TestApi

urlpatterns = [
    path('auth/', include('authentication.urls')),
    path('users/', include('users.urls')),
    path('test/', TestApi.as_view()),
]
