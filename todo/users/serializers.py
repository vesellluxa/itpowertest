from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token

from users.models import ToDoUser


class ToDoUserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=128,
                                     required=True,
                                     write_only=True)

    class Meta:
        model = ToDoUser
        fields = ('email', 'first_name', 'last_name', 'password')

    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**validated_data)
        return user


class TokenObtainSerializer(serializers.Serializer):
    password = serializers.CharField()
    email = serializers.EmailField()

    def validate(self, data):
        email = data.get('email')
        if not ToDoUser.objects.filter(email=email).exists():
            raise ValidationError('Email is invalid')
        user = ToDoUser.objects.filter(email=email).first()
        raw_password = data.get('password')
        if not user.check_password(raw_password):
            raise ValidationError('Password is invalid')
        return data

    def get_or_create_token(self):
        user = ToDoUser.objects.get(email=self.data.get('email'))
        token = Token.objects.get_or_create(user=user)[0]
        return token
