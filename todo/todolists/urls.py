from rest_framework import routers

from todolists.views import TagViewSet, CaseViewSet, ToDoListViewSet


router = routers.DefaultRouter()
router.register(
    'tags',
    TagViewSet,
    basename='tags')
router.register(
    'cases',
    CaseViewSet,
    basename='cases')
router.register(
    'todolists',
    ToDoListViewSet,
    basename='todolists')
urlpatterns = [] + router.urls
