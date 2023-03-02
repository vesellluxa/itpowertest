from django.contrib import admin

from todolists.models import Tag, Case, ToDoList

admin.site.register(Tag)
admin.site.register(Case)
admin.site.register(ToDoList)
