from rest_framework import serializers

from todolists.models import Tag, Case, ToDoList
from todo.settings import DATETIME_FORMAT


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

    def create(self, validated_data):
        cases = Case.objects.filter(id__in=validated_data.pop('cases'))
        obj = self.Meta.model.objects.create(
            owner=self.context.get('request').user, **validated_data)
        obj.cases.set(cases)
        return obj
