from datetime import datetime

from django.db import models
from pytz import utc

from users.models import ToDoUser


class Tag(models.Model):
    title = models.CharField(verbose_name='Название',
                             max_length=100,
                             blank=False,
                             unique=True)
    slug = models.CharField(verbose_name='Идентификатор',
                            max_length=100, unique=True)


class Case(models.Model):
    title = models.CharField(verbose_name='Название',
                             max_length=100,
                             blank=False)
    description = models.CharField(verbose_name='Описание',
                                   max_length=500,
                                   blank=False)
    solved = models.BooleanField(verbose_name='Закрыт ли?',
                                 default=False)
    deadline = models.DateTimeField(verbose_name='Дедлайн')
    tag = models.ForeignKey(verbose_name='Тэг',
                            to=Tag,
                            on_delete=models.PROTECT)
    owner = models.ForeignKey(to=ToDoUser,
                              on_delete=models.CASCADE)

    def is_expired(self):
        return utc.localize(datetime.now()) > self.deadline


class ToDoList(models.Model):
    title = models.CharField(verbose_name='Название',
                             blank=False,
                             max_length=100)
    owner = models.ForeignKey(to=ToDoUser,
                              on_delete=models.CASCADE)
    cases = models.ManyToManyField(verbose_name='Дела',
                                   to=Case)
