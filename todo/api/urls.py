from django.urls import path, include
from rest_framework import routers

from api.views import (obtain_token, logout, ToDoUserViewSet,
                       TagViewSet, CaseViewSet, ToDoListViewSet)

router = routers.DefaultRouter()

router.register('users',
                ToDoUserViewSet, basename='users')

router.register('tags',
                TagViewSet, basename='tags')

router.register('cases',
                CaseViewSet, basename='cases')

router.register('todolists',
                ToDoListViewSet, basename='todolists')

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/obtain_token/', obtain_token),
    path('v1/logout/', logout)
]
