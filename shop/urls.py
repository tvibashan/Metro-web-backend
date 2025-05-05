from django.urls import include, path

from .views import (
    OptionViewSet,
    ProductViewSet,
    BookingViewSet,
    ReviewViewSet,
    WishListViewSet,
    toursView,
    dashboard_data,
    toursDetailView,
    toursfilterView,
    toursPaymentView,
    createBookingDetailView,
    checkAvailabilityDetailView,
    check_booking_qr_code_validation,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register("products", ProductViewSet, basename="product")
router.register("options", OptionViewSet, basename="option")
router.register("wishlists", WishListViewSet, basename="wishlist")
router.register("bookings", BookingViewSet, basename="booking")
router.register("reviews", ReviewViewSet, basename="review")


app_name = "shop" 

urlpatterns = [
    path("tours/", toursView, name="tour"),
    path("tours-filter/", toursfilterView, name="tour"),
    path("tours/<str:api_type>/<str:id>/", toursDetailView, name="tour-detail"),
    path(
        "tours/<str:api_type>/<str:id>/available/",
        checkAvailabilityDetailView,
        name="tour-check-with-date",
    ),
    path(
        "tours/<str:api_type>/create/bookings/",
        createBookingDetailView,
        name="tour-with-reservation-id",
    ),
    path("tours/payment/", toursPaymentView, name="tour-payment"),
    path(
        "validate-qr-code/",
        check_booking_qr_code_validation,
        name="check_booking_qr_code_validation",
    ),
    path('invalidate-qr-code/', invalidate_booking_qr_code, name='invalidate_booking_qr_code'),
    path("dashboard-data/", dashboard_data, name="dashboard-data"),
    path("", include(router.urls)),
]

