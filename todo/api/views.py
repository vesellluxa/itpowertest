from django_filters.rest_framework.backends import DjangoFilterBackend
from rest_framework.viewsets import ModelViewSet
from rest_framework import mixins, status
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from api.serializers import (TagSerializer, CaseSerializer,
                             ToDoListSerializer, ToDoUserSerializer,
                             TokenObtainSerializer)
from api.filters import TagFilter
from todolists.models import Tag, Case, ToDoList


class CaseViewSet(ModelViewSet):
    serializer_class = CaseSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TagFilter

    def get_queryset(self):
        return Case.objects.filter(owner=self.request.user)

    @action(
        methods=['POST'],
        detail=True,
        permission_classes=(IsAuthenticated,)
    )
    def solve(self, request, pk):
        case = Case.objects.filter(pk=pk).first()
        case.solved = True
        case.save()
        return Response("Case solved!", status=status.HTTP_200_OK)


class ToDoListViewSet(ModelViewSet):
    serializer_class = ToDoListSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return ToDoList.objects.filter(owner=self.request.user)



class TagViewSet(mixins.ListModelMixin,
                 mixins.RetrieveModelMixin,
                 GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = None
    permission_classes = (IsAuthenticated,)


class ToDoUserViewSet(mixins.CreateModelMixin,
                      GenericViewSet):
    serializer_class = ToDoUserSerializer

    @action(
        methods=['GET', 'DELETE'],
        detail=False,
        permission_classes=(IsAuthenticated,)
    )
    def me(self, request):
        user = request.user
        if request.method == 'DELETE':
            user.delete()
            return Response('your account has been deleted',
                            status=status.HTTP_204_NO_CONTENT)
        serializer = self.get_serializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
def obtain_token(request):
    serializer = TokenObtainSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    token = serializer.get_or_create_token()
    return Response(
        data={"auth_token": f"{token}"},
        status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout(request):
    request.user.auth_token.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
