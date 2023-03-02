from django.urls import path, include
from rest_framework import routers

from users.views import ToDoUserViewSet, obtain_token, logout


router = routers.DefaultRouter()
router.register(
    'users',
    ToDoUserViewSet,
    basename='users')

urlpatterns = [
    path('', include(router.urls)),
    path('api_token_auth/', obtain_token),
    path('logout/', logout)
]
