import django_filters as filters

from todolists.models import Case


class TagFilter(filters.FilterSet):
    tag = filters.CharFilter(field_name='tag__slug',
                             lookup_expr='icontains')
    title = filters.CharFilter(field_name='title',
                              lookup_expr='icontains')

    class Meta:
        model = Case
        fields = ('title', 'tag')
