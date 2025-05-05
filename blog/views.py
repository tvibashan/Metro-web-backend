from ast import literal_eval
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.pagination import PageNumberPagination
from blog.serializers import (
    BlogChangeSerializer,
    BlogDetailSerializer,
    BlogListSerializer,
    CategorySerializer,
    TagSerializer,
)
from .models import BlogImage, Category, Blog, Tags


class BlogPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = "page_size"
    max_page_size = 100


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    permission_classes = [IsAuthenticatedOrReadOnly]
    filterset_fields = []
    search_fields = ["name"]
    ordering_fields = ["name"]
    ordering = ["name"]


class BlogViewSet(viewsets.ModelViewSet):
    queryset = Blog.objects.all().order_by("-created_at")
    search_fields = ["title", "details"]
    ordering_fields = ["created_at", "title"]
    permission_classes = [IsAuthenticatedOrReadOnly]
    pagination_class = BlogPagination
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ["category", "tags", "tags__name"]
    search_fields = ["title", "category__name", "tags__name"]
    ordering_fields = ["created_at", "title"]
    ordering = ["-created_at"]

    def get_serializer_class(self):
        if self.action == "retrieve":
            return BlogDetailSerializer
        elif self.action == "list":
            return BlogListSerializer
        return BlogChangeSerializer

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", "destroy"]:
            return [IsAdminUser()]
        return super().get_permissions()

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        blog = self.get_object()

        related_blogs = Blog.objects.filter(category=blog.category).exclude(id=blog.id)[
            :4
        ]
        related_serializer = BlogListSerializer(
            related_blogs, many=True, context={"request": request}
        )

        response.data["related_blogs"] = related_serializer.data
        return response

    def perform_create(self, serializer):
        blog = serializer.save()

        images_data = self.request.FILES.getlist("images", [])
        tags_data = self.request.data.get("tags", [])

        if isinstance(tags_data, str):
            tags_data = literal_eval(tags_data)
        tags_data = [int(tag_id) for tag_id in tags_data]

        for image in images_data:
            BlogImage.objects.create(blog=blog, image=image)

        tags = Tags.objects.filter(id__in=tags_data)
        blog.tags.set(tags)

        return blog

    def perform_update(self, serializer):
        blog = serializer.save()
        images_data = self.request.FILES.getlist("images", [])
        tags_data = self.request.data.get("tags", [])

        if isinstance(tags_data, str):
            tags_data = literal_eval(tags_data)
        tags_data = [int(tag_id) for tag_id in tags_data]

        if "delete_images" in self.request.data:
            delete_image_ids = self.request.data.getlist("delete_images", [])
            blog.images.filter(id__in=delete_image_ids).delete()

        for image in images_data:
            BlogImage.objects.create(blog=blog, image=image)

        tags = Tags.objects.filter(id__in=tags_data)
        blog.tags.set(tags)

        return blog


class TagViewSet(viewsets.ModelViewSet):
    queryset = Tags.objects.all()
    serializer_class = TagSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
