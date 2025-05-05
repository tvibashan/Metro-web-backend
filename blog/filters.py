from django_filters import rest_framework as filters

from .models import Blog


class BlogFilter(filters.FilterSet):
    category = filters.CharFilter(field_name="category__name", lookup_expr='icontains')
    slug = filters.CharFilter(field_name="slug", lookup_expr='icontains')
    tags = filters.CharFilter(field_name="tags__name", lookup_expr='icontains')


    class Meta: 
        model = Blog
        fields = ['category','tags','slug']

