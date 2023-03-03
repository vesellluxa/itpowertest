from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.authtoken.models import Token

from todolists.models import Tag, Case, ToDoList
from todo.settings import DATETIME_FORMAT
from users.models import ToDoUser


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = '__all__'


class RepresentCaseSerializer(serializers.ModelSerializer):
    tag = TagSerializer()
    is_expired = serializers.SerializerMethodField()

    class Meta:
        model = Case
        fields = ('pk', 'title', 'solved', 'is_expired', 'deadline', 'tag')

    def get_is_expired(self, instance):
        return instance.is_expired()


class CaseSerializer(serializers.ModelSerializer):
    tag = serializers.IntegerField()
    deadline = serializers.DateTimeField(format=DATETIME_FORMAT, input_formats=None)

    class Meta:
        model = Case
        fields = ('pk', 'title', 'description', 'solved', 'deadline', 'tag')

    def to_representation(self, instance):
        serializer = RepresentCaseSerializer(
            instance,
            context={'request': self.context.get('request')}
        )
        return serializer.data

    def create(self, validated_data):
        tag = Tag.objects.filter(pk=validated_data.pop('tag')).first()
        obj = self.Meta.model.objects.create(
            owner=self.context.get('request').user, tag=tag, **validated_data)
        return obj


class RepresentToDoListSerializer(serializers.ModelSerializer):
    cases = RepresentCaseSerializer(many=True)

    class Meta:
        model = ToDoList
        fields = ('title', 'cases')


class ToDoListSerializer(serializers.ModelSerializer):
    cases = serializers.ListField()

    class Meta:
        model = ToDoList
        fields = ('title', 'cases')

    def to_representation(self, instance):
        serializer = RepresentToDoListSerializer(
            instance,
            context={'request': self.context.get('request')})
        return serializer.data

    def validate_cases(self, values):
        for value in values:
            if not Case.objects.filter(pk=value).first():
                raise ValidationError('Not valid case ID!')
        return values

    def create(self, validated_data):
        cases = Case.objects.filter(id__in=validated_data.pop('cases'))
        obj = self.Meta.model.objects.create(
            owner=self.context.get('request').user, **validated_data)
        obj.cases.set(cases)
        return obj


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
        user = ToDoUser.objects.filter(email=email).first()
        if not user:
            raise ValidationError('Email is invalid')
        raw_password = data.get('password')
        if not user.check_password(raw_password):
            raise ValidationError('Password is invalid')
        return data

    def get_or_create_token(self):
        user = ToDoUser.objects.get(email=self.data.get('email'))
        token = Token.objects.get_or_create(user=user)[0]
        return token
