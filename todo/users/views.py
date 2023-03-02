from django.shortcuts import render
from rest_framework import mixins, status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.decorators import action, api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from users.serializers import ToDoUserSerializer, TokenObtainSerializer


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
