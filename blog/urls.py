from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CategoryViewSet, BlogViewSet, TagViewSet

router = DefaultRouter()
router.register("categories", CategoryViewSet, basename="category")
router.register("blogs", BlogViewSet, basename="blog")
router.register("tags", TagViewSet, basename="tag")

app_name = "blog"

# URL patterns
urlpatterns = [
    path("", include(router.urls)),
]
