from django.contrib.auth import get_user_model
from djoser.serializers import (
    UserCreateSerializer as BaseUserCreateSerializer,
    UserSerializer as BaseUserSerializer,
)
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

from shop.serializers import GetBookingSerializer, ReviewSerializer
from shop.models import Booking, Review
from rest_framework import serializers

User = get_user_model()


class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = [
            "id",
            "email",
            "password",
            "date_of_birth",
            "phone",
            "address",
            "city",
            "country",
            "blood_group",
            "first_name",
            "last_name",
            "image",
        ]


class UserSerializer(BaseUserSerializer):
    total_bookings = serializers.SerializerMethodField()
    reserved_bookings = serializers.SerializerMethodField()
    confirmed_bookings = serializers.SerializerMethodField()
    cancelled_bookings = serializers.SerializerMethodField()
    recent_bookings = serializers.SerializerMethodField()
    recent_reviews = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "phone",
            "image",
            "address",
            "city",
            "country",
            "blood_group",
            "total_bookings",
            "reserved_bookings",
            "confirmed_bookings",
            "cancelled_bookings",
            "recent_bookings",
            "recent_reviews",
        ]

    def get_total_bookings(self, obj):
        return Booking.objects.filter(user=obj).count()

    def get_reserved_bookings(self, obj):
        return Booking.objects.filter(user=obj, status="Reserved").count()

    def get_confirmed_bookings(self, obj):
        return Booking.objects.filter(user=obj, status="Confirmed").count()

    def get_cancelled_bookings(self, obj):
        return Booking.objects.filter(user=obj, status="Cancelled").count()

    def get_recent_bookings(self, obj):
        recent_bookings = Booking.objects.filter(user=obj).order_by(
            "-departure_date_time"
        )[:3]
        return GetBookingSerializer(recent_bookings, many=True).data

    def get_recent_reviews(self, obj):
        recent_reviews = Review.objects.filter(user=obj).order_by("-created_at")[:6]
        return ReviewSerializer(recent_reviews, many=True).data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        return token


class UserListSerializer(serializers.ModelSerializer):
    total_bookings = serializers.SerializerMethodField()
    reserved_bookings = serializers.SerializerMethodField()
    confirmed_bookings = serializers.SerializerMethodField()
    cancelled_bookings = serializers.SerializerMethodField()
    recent_reviews = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "phone",
            "image",
            "address",
            "city",
            "country",
            "blood_group",
            "total_bookings",
            "reserved_bookings",
            "confirmed_bookings",
            "cancelled_bookings",
            "recent_reviews",
        ]

    def get_total_bookings(self, obj):
        return Booking.objects.filter(user=obj).count()

    def get_reserved_bookings(self, obj):
        return Booking.objects.filter(user=obj, status="Reserved").count()

    def get_confirmed_bookings(self, obj):
        return Booking.objects.filter(user=obj, status="Confirmed").count()

    def get_cancelled_bookings(self, obj):
        return Booking.objects.filter(user=obj, status="Cancelled").count()

    def get_recent_reviews(self, obj):
        recent_reviews = Review.objects.filter(user=obj).order_by("-created_at")[:6]
        return ReviewSerializer(recent_reviews, many=True).data
 

class UserDetailSerializer(serializers.ModelSerializer):
    total_bookings = serializers.SerializerMethodField()
    reserved_bookings = serializers.SerializerMethodField()
    confirmed_bookings = serializers.SerializerMethodField()
    cancelled_bookings = serializers.SerializerMethodField()
    recent_bookings = serializers.SerializerMethodField()
    all_bookings = serializers.SerializerMethodField()
    recent_reviews = serializers.SerializerMethodField()

    class Meta(BaseUserSerializer.Meta):
        model = User
        fields = [
            "id",
            "first_name",
            "last_name",
            "email",
            "date_of_birth",
            "phone",
            "image",
            "address",
            "city",
            "country",
            "blood_group",
            "total_bookings",
            "reserved_bookings",
            "confirmed_bookings",
            "cancelled_bookings",
            "recent_bookings",
            "all_bookings",
            "recent_reviews",
        ]

    def get_total_bookings(self, obj):
        return Booking.objects.filter(user=obj).count()

    def get_reserved_bookings(self, obj):
        return Booking.objects.filter(user=obj, status="Reserved").count()

    def get_confirmed_bookings(self, obj):
        return Booking.objects.filter(user=obj, status="Confirmed").count()

    def get_cancelled_bookings(self, obj):
        return Booking.objects.filter(user=obj, status="Cancelled").count()

    def get_recent_bookings(self, obj):
        recent_bookings = Booking.objects.filter(user=obj).order_by(
            "-departure_date_time"
        )[:3]
        return GetBookingSerializer(recent_bookings, many=True).data 

    def get_all_bookings(self, obj):
        all_bookings = Booking.objects.filter(user=obj).order_by("-departure_date_time")
        return GetBookingSerializer(all_bookings, many=True).data

    def get_recent_reviews(self, obj):
        recent_reviews = Review.objects.filter(user=obj).order_by("-created_at")[:6]
        return ReviewSerializer(recent_reviews, many=True).data
 