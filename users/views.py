from rest_framework import viewsets
from rest_framework.filters import OrderingFilter, SearchFilter
from blog.views import BlogPagination
from .models import User
from .serializers import UserCreateSerializer, UserListSerializer, UserDetailSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    pagination_class = BlogPagination
    filter_backends = [SearchFilter, OrderingFilter]
    search_fields = ["email", "first_name", "last_name", "phone"]
    ordering_fields = ["email", "first_name", "last_name", "date_of_birth", "id"]
    ordering = ["id"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return UserDetailSerializer
        elif self.action == "list":
            return UserListSerializer
        return UserListSerializer
