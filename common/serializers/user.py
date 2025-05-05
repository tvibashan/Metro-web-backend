from rest_framework import serializers
from users.models import User
from shop.models import Booking
from djoser.serializers import (
    UserSerializer as BaseUserSerializer,
)


class UserListSerializer(serializers.ModelSerializer):
    total_bookings = serializers.SerializerMethodField()
    reserved_bookings = serializers.SerializerMethodField()
    confirmed_bookings = serializers.SerializerMethodField()
    cancelled_bookings = serializers.SerializerMethodField()

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
        ]

    def get_total_bookings(self, obj):
        return Booking.objects.filter(user=obj).count()

    def get_reserved_bookings(self, obj):
        return Booking.objects.filter(user=obj, status="Reserved").count()

    def get_confirmed_bookings(self, obj):
        return Booking.objects.filter(user=obj, status="Confirmed").count()

    def get_cancelled_bookings(self, obj):
        return Booking.objects.filter(user=obj, status="Cancelled").count()
