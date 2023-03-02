from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import GenericViewSet, ModelViewSet

from todolists.models import Tag, Case, ToDoList
from todolists.serializers import TagSerializer, CaseSerializer, ToDoListSerializer


class CaseViewSet(ModelViewSet):
    serializer_class = CaseSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return Case.objects.filter(owner=self.request.user)


class ToDoListViewSet(ModelViewSet):
    serializer_class = ToDoListSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated, )

    def get_queryset(self):
        return ToDoList.objects.filter(owner=self.request.user)


class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated, )

