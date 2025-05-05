from rest_framework import serializers
from .models import Category, Blog, BlogImage, Reel, Tags


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name"]


class BlogImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogImage
        fields = ["id", "image"]


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ["id", "name"]


class ReelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Reel
        fields = [
            "title",
            "video",
            "caption",
            "created_at",
        ]


class BlogListSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    images = BlogImageSerializer(many=True, required=False)
    tags = TagSerializer(many=True, required=False)

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "short_desc",
            "category",
            "created_at",
            "images",
            "tags",
        ]


class BlogDetailSerializer(serializers.ModelSerializer):
    images = BlogImageSerializer(many=True, required=False)
    tags = TagSerializer(many=True, required=False)
    category = CategorySerializer()

    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "short_desc",
            "details",
            "category",
            "images",
            "tags",
            "created_at",
            "updated_at",
        ]


class BlogChangeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = [
            "id",
            "title",
            "slug",
            "short_desc",
            "details",
            "category",
            "created_at",
            "updated_at",
        ]
