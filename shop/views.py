# from decimal import Decimal
# import os
# from django.shortcuts import get_object_or_404
# from rest_framework import status, mixins, viewsets
# from rest_framework.parsers import MultiPartParser, FormParser
# from rest_framework.decorators import api_view, permission_classes, action
# from datetime import timedelta
# from django.utils import timezone
# from rest_framework.response import Response
# from rest_framework.exceptions import APIException
# from rest_framework.permissions import AllowAny, IsAuthenticated
# from blog.views import BlogPagination
# from rest_framework import serializers

# from users.models import User
# from shop.serializers import (
#     BookingCreateUpdateSerializer,
#     BookingDetailSerializer,
#     BookingListSerializer,
#     GetBookingSerializer,
#     OptionCreateUpdateSerializer,
#     OptionListSerializer,
#     ProductCreateUpdateSerializer,
#     ProductDetailSerializer,
#     ProductSerializer,
#     ReviewCreateSerializer,
#     ReviewSerializer,
#     WishlistSerializer,
# )
# from django_filters.rest_framework import DjangoFilterBackend
# from rest_framework.filters import OrderingFilter, SearchFilter
# from shop.models import Booking, Option, Product, Review, Wishlist, WishlistItem
# from .apis.base import BaseAPI
# from django.db import transaction
# from django.db.models import Sum, Count, Q, Min

# from django.utils.timezone import now


# SITE_URL = os.environ.get("SITE_URL")
# API_URL = os.environ.get("API_URL")


# @api_view(["POST"])
# @permission_classes([AllowAny])
# def toursPaymentView(request):
#     try:
#         payment_method = request.data.get("payment_method")
#         api_type = request.data.get("api_type", "g")
#         booking_id = request.data.get("id")

#         return_url = f"{SITE_URL}/checkout/{booking_id}/success"
#         booking = None

#         if api_type.upper() == "G":
#             booking = get_object_or_404(Booking, id=booking_id)
#         else:
#             return Response(
#                 {"error": "Invalid Api Type", "success": False},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         if booking and booking.status not in ["Confirmed", "Cancelled"]:
#             try:
#                 payment_intent = stripe.PaymentIntent.create(
#                     amount=int(float(booking.total_amount) * 100),
#                     currency="usd",
#                     description="Geeky Tours",
#                     payment_method=payment_method,
#                     receipt_email=booking.user.email,
#                     confirm=True,
#                     return_url=return_url,
#                 )
#                 if payment_intent.status == "succeeded":
#                     # sendPaymentMail(
#                     #     booking.user.email,
#                     #     booking.product_title,
#                     #     booking_id,
#                     #     booking.total_amount,
#                     # )
#                     tour = BaseAPI.update_detail_booking(
#                         api_type=api_type, booking_id=booking_id
#                     )
#                     return Response(tour, status=status.HTTP_200_OK)
#                 else:
#                     serializer = GetBookingSerializer(booking).data
#                     return Response(
#                         {"data": serializer, "success": False},
#                         status=status.HTTP_400_BAD_REQUEST,
#                     )
#             except stripe.error.StripeError as e:
#                 error_message = str(e)
#                 return Response(
#                     {"error": error_message, "success": False},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#             except Exception as e:
#                 error_message = str(e)
#                 return Response(
#                     {"error": error_message, "success": False},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )
#         else:
#             return Response(
#                 {"error": "already paid or confirmed", "success": False},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )
#     except APIException as e:
#         print("APIException:", e)
#         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         print("Exception:", e)
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(["GET"])
# @permission_classes([AllowAny])
# def toursView(request):
#     try:
#         tours = BaseAPI.get_all_tours(request=request)
#         return Response(tours, status=status.HTTP_200_OK)
#     except APIException as e:
#         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(["GET", "POST"])
# @permission_classes([AllowAny])
# def toursDetailView(request, api_type, id):
#     try:
#         tour = BaseAPI.get_tour_detail(api_type=api_type, id=id, request=request)
#         return Response(tour, status=status.HTTP_200_OK)
#     except APIException as e:
#         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(["GET", "POST"])
# @permission_classes([AllowAny])
# def checkAvailabilityDetailView(request, api_type, id):
#     try:
#         if api_type.upper() == "G":
#             data = request.data
#             requested_date = data.get("date")

#             payload = {"requested_date": requested_date}

#             if not requested_date:
#                 return Response(
#                     {"error": "Missing date"},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#             tour = BaseAPI.check_availability(api_type=api_type, id=id, data=payload)
#             return Response(tour, status=status.HTTP_200_OK)

#         return Response(
#             {"error": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST
#         )
#     except APIException as e:
#         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(["POST", "GET", "PATCH"])
# @permission_classes([IsAuthenticated])
# def createBookingDetailView(request, api_type):
#     if request.method == "POST":
#         try:
#             if api_type.upper() == "G":
#                 user = request.user.id
#                 data = request.data
#                 data["user_id"] = user
#                 tour = BaseAPI.create_booking(api_type=api_type, data=data)
#                 return Response(tour, status=status.HTTP_200_OK)

#             else:
#                 return Response(
#                     {"error": "Invalid Request"}, status=status.HTTP_400_BAD_REQUEST
#                 )
#         except APIException as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#     if request.method == "GET":
#         try:
#             booking_id = request.query_params.get("booking_id")
#             if booking_id:
#                 tours = BaseAPI.get_detail_booking(
#                     api_type=api_type, booking_id=booking_id
#                 )
#                 return Response(tours, status=status.HTTP_200_OK)
#             else:
#                 bookings = Booking.objects.filter(user=request.user).order_by(
#                     "-updated_at"
#                 )
#                 bookings_serializer = GetBookingSerializer(bookings, many=True).data
#                 return Response(
#                     {"data": bookings_serializer, "success": True},
#                     status=status.HTTP_200_OK,
#                 )

#         except APIException as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

#     if request.method == "PATCH":
#         try:
#             reservation_id = request.query_params.get("reservation_id")
#             data = request.data.get("data")
#             if api_type.upper() == "V":
#                 booking_data = request.data.get("booking_data")
#                 tours = BaseAPI.update_detail_booking(
#                     api_type=api_type,
#                     reservation_id=reservation_id,
#                     api_data=data,
#                     booking_data=booking_data,
#                 )
#                 if "error" in tours["data"]:
#                     return Response(tours, status=status.HTTP_400_BAD_REQUEST)
#                 else:
#                     return Response(tours, status=status.HTTP_200_OK)

#             if api_type.upper() == "T":
#                 booking_data = request.data.get("booking_data")
#                 tours = BaseAPI.confirm_detail_booking(
#                     api_type=api_type,
#                     reservation_id=reservation_id,
#                     booking_data=booking_data,
#                 )
#                 if "error" in tours["data"]:
#                     return Response(tours, status=status.HTTP_400_BAD_REQUEST)
#                 else:
#                     return Response(tours, status=status.HTTP_200_OK)

#             tours = BaseAPI.update_detail_booking(
#                 api_type=api_type, reservation_id=reservation_id, api_data=data
#             )
#             return Response(tours, status=status.HTTP_200_OK)
#         except APIException as e:
#             print("APIException:", e)
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#         except Exception as e:
#             print("Exception:", e)
#             return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)


# class ReviewViewSet(viewsets.ModelViewSet):
#     http_method_names = ["get", "post", "patch", "delete", "head", "options"]
#     permission_classes = [IsAuthenticated]
#     pagination_class = BlogPagination
#     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
#     filterset_fields = [
#         "user",
#         "rating",
#     ]
#     search_fields = [
#         "product_title",
#         "user__email",
#     ]
#     ordering_fields = [
#         "product_title",
#         "user__email",
#         "created_at",
#         "basePrice",
#     ]
#     ordering = ["-created_at"]

#     def get_serializer_class(self):
#         if self.request.method == "POST":
#             return ReviewCreateSerializer
#         return ReviewSerializer

#     def get_queryset(self):
#         user_id = self.request.user.id
#         user = User.objects.get(id=user_id)
#         if user.is_staff or user.is_superuser:
#             return Review.objects.all()
#         return Review.objects.filter(user=user)

#     def perform_create(self, serializer):
#         user = self.request.user
#         api_category = self.request.data.get("api_category", "g").upper()
#         product_id = self.request.data.get("product_id")

#         if not product_id:
#             raise serializers.ValidationError({"error": "Product ID is required."})

#         product_title = product_image = product_duration = product_location = (
#             product_price
#         ) = None

#         if api_category == "G":
#             product = (
#                 Product.objects.filter(pk=product_id).prefetch_related("images").first()
#             )
#             if not product:
#                 raise serializers.ValidationError({"error": "Product not found."})

#             product_title = product.title
#             product_duration = product.duration
#             product_location = product.location
#             product_price = product.basePrice
#             product_image = (
#                 self.request.build_absolute_uri(product.images.first().image.url)
#                 if product.images.exists()
#                 else None
#             )
#         else:
#             product_title = self.request.data.get("product_title")
#             product_image = self.request.data.get("product_image")
#             product_duration = self.request.data.get("product_duration")
#             product_location = self.request.data.get("product_location")
#             product_price = self.request.data.get("product_price")

#             missing_fields = [
#                 field
#                 for field in ["product_title", "product_image"]
#                 if not locals().get(field)
#             ]
#             if missing_fields:
#                 raise serializers.ValidationError(
#                     {"error": f"Missing required fields: {', '.join(missing_fields)}."}
#                 )

#         serializer.save(
#             user=user,
#             api_category=api_category,
#             product_id=product_id,
#             product_title=product_title,
#             product_image=product_image,
#             product_duration=product_duration,
#             product_location=product_location,
#             product_price=product_price,
#         )


# class WishListViewSet(viewsets.ModelViewSet):
#     http_method_names = ["get", "post", "patch", "delete", "head", "options"]
#     permission_classes = [IsAuthenticated]

#     def get_serializer_class(self):
#         if self.request.method == "GET":
#             return WishlistSerializer
#         return WishlistSerializer

#     def get_queryset(self):
#         user_id = self.request.user.id
#         user = User.objects.get(id=user_id)
#         return Wishlist.objects.filter(user=user)

#     def list(self, request, *args, **kwargs):
#         queryset = self.get_queryset()
#         serializer = self.get_serializer(queryset, many=True)

#         if not serializer.data:
#             return Response({"data": []}, status=status.HTTP_200_OK)

#         return Response(serializer.data, status=status.HTTP_200_OK)

#     @action(
#         detail=False,
#         methods=["POST"],
#         permission_classes=[IsAuthenticated],
#         url_path="toggle-wishlist",
#     )
#     def toggle_wishlistitem(self, request):
#         user = request.user
#         product_id = request.data.get("product_id")
#         api_type = request.data.get("api_type", "g").upper()

#         if not product_id:
#             return Response(
#                 {"error": "Missing required field: product_id."},
#                 status=status.HTTP_400_BAD_REQUEST,
#             )

#         product_title = product_image = product_duration = product_location = (
#             product_price
#         ) = None

#         if api_type == "G":
#             product = Product.objects.filter(pk=product_id).first()
#             if not product:
#                 return Response(
#                     {"error": "Product not found."},
#                     status=status.HTTP_404_NOT_FOUND,
#                 )
#             product_title = product.title
#             product_duration = product.duration
#             product_location = product.location
#             product_price = product.get_discounted_price()
#             product_image = (
#                 product.images.first().image.url if product.images.exists() else None
#             )
#         else:
#             product_title = request.data.get("product_title")
#             product_image = request.data.get("product_image")
#             product_duration = request.data.get("product_duration")
#             product_location = request.data.get("product_location")
#             product_price = request.data.get("product_price")

#             missing_fields = [
#                 field
#                 for field in ["product_title", "product_image"]
#                 if not locals().get(field)
#             ]
#             if missing_fields:
#                 return Response(
#                     {"error": f"Missing required fields: {', '.join(missing_fields)}."},
#                     status=status.HTTP_400_BAD_REQUEST,
#                 )

#         wishlist_item = WishlistItem.objects.filter(
#             wishlist__user=user, product_id=product_id, api_category=api_type
#         ).first()

#         if wishlist_item:
#             wishlist_item.delete()
#             message, created = "Product removed from wishlist.", False
#         else:
#             wishlist, _ = Wishlist.objects.get_or_create(user=user)
#             WishlistItem.objects.create(
#                 wishlist=wishlist,
#                 product_id=product_id,
#                 product_title=product_title,
#                 product_image=product_image,
#                 product_duration=product_duration,
#                 product_location=product_location,
#                 product_price=product_price,
#                 api_category=api_type,
#             )
#             message, created = "Product added to wishlist.", True

#         return Response(
#             {"message": message, "created": created}, status=status.HTTP_200_OK
#         )


# @api_view(["POST"])
# @permission_classes([AllowAny])
# def toursfilterView(request):
#     try:
#         category = request.data.get("category", "")
#         search = request.data.get("search", "")
#         sort = request.data.get("sort", "")
#         page = request.data.get("page", "")

#         tours = BaseAPI.get_filter_tours(
#             search=search,
#             sort=sort,
#             page=page,
#             request=request,
#             category=category,
#         )
#         return Response(tours, status=status.HTTP_200_OK)
#     except ValueError as e:
#         print("ValueError:", e)
#         return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
#     except Exception as e:
#         print("Exception:", e)
#         return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# @api_view(["POST"])
# @permission_classes([AllowAny])
# def check_booking_qr_code_validation(request):
#     if request.method == "POST":
#         booking_id = request.data.get("booking_id")
#         if booking_id:
#             try:
#                 booking = Booking.objects.get(booking_id=booking_id)
#                 if booking.departure_date:
#                     departure_date = booking.departure_date.date()
#                     current_date = timezone.now().date()
#                     departure_date_plus_3_days = departure_date + timedelta(days=3)
#                     if current_date <= departure_date_plus_3_days and booking.is_valid:
#                         return Response({"valid": True})
#                     else:
#                         return Response({"valid": False})
#                 else:
#                     return Response(
#                         {
#                             "valid": False,
#                             "message": "Departure date not provided for the booking.",
#                         }
#                     )
#             except Booking.DoesNotExist:
#                 return Response({"valid": False, "message": "Booking does not exist."})
#         else:
#             return Response({"valid": False, "message": "Booking ID not provided."})
#     else:
#         return Response({"error": "Only POST requests are allowed."}, status=405)


# # @api_view(["PATCH"])
# # @permission_classes([IsDriver])
# # def invalidate_booking_qr_code(request):
# #     if request.method == "PATCH":
# #         booking_id = request.data.get("booking_id")
# #         if booking_id:
# #             try:
# #                 booking = Booking.objects.get(booking_id=booking_id)
# #                 if booking.is_valid:
# #                     departure_datetime = datetime.strptime(
# #                         booking.departure_date_time, "%Y-%m-%d, %H:%M"
# #                     )
# #                     rome_tz = pytz.timezone("Europe/Rome")
# #                     departure_datetime_rome = rome_tz.localize(departure_datetime)
# #                     current_datetime_rome = timezone.now().astimezone(rome_tz)

# #                     extended_validity_time = departure_datetime_rome + timedelta(
# #                         hours=1
# #                     )

# #                     if current_datetime_rome > extended_validity_time:
# #                         return Response(
# #                             {
# #                                 "error": f"Booking with ID {booking_id} has already expired and cannot be invalidated."
# #                             },
# #                             status=status.HTTP_400_BAD_REQUEST,
# #                         )

# #                     booking.is_valid = False
# #                     booking.ticket_checker = request.user.email
# #                     booking.save()
# #                     return Response(
# #                         {
# #                             "message": f"Booking with ID {booking_id} has been successfully invalidated."
# #                         }
# #                     )
# #                 else:
# #                     return Response(
# #                         {"error": f"Booking with ID {booking_id} is already invalid."},
# #                         status=status.HTTP_400_BAD_REQUEST,
# #                     )
# #             except Booking.DoesNotExist:
# #                 return Response(
# #                     {"error": f"Booking with ID {booking_id} does not exist."},
# #                     status=status.HTTP_404_NOT_FOUND,
# #                 )
# #         else:
# #             return Response(
# #                 {"error": "Booking ID not provided."},
# #                 status=status.HTTP_400_BAD_REQUEST,
# #             )
# #     else:
# #         return Response(
# #             {"error": "Method is not allowed."},
# #             status=status.HTTP_405_METHOD_NOT_ALLOWED,
# #         )


# # ----------------------------------------------------------------------------------------------------------------------------------------------------


# class OptionViewSet(
#     mixins.ListModelMixin,
#     mixins.CreateModelMixin,
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     viewsets.GenericViewSet,
# ):
#     queryset = Option.objects.all()
#     permission_classes = [AllowAny]

#     def get_serializer_class(self):
#         if self.action in ["list"]:
#             return OptionListSerializer
#         elif self.action in ["retrieve"]:
#             return OptionListSerializer
#         return OptionCreateUpdateSerializer

#     def create(self, request, *args, **kwargs):
#         with transaction.atomic():
#             return super().create(request, *args, **kwargs)

#     def update(self, request, *args, **kwargs):
#         with transaction.atomic():
#             return super().update(request, *args, **kwargs)

#     def partial_update(self, request, *args, **kwargs):
#         with transaction.atomic():
#             return super().partial_update(request, *args, **kwargs)


# class ProductViewSet(
#     mixins.ListModelMixin,
#     mixins.CreateModelMixin,
#     mixins.RetrieveModelMixin,
#     mixins.UpdateModelMixin,
#     viewsets.GenericViewSet,
# ):
#     queryset = Product.objects.all()
#     permission_classes = [AllowAny]
#     pagination_class = BlogPagination
#     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
#     filterset_fields = [
#         "languageType",
#         "category",
#         "status",
#         "isFoodIncluded",
#         "isTransportIncluded",
#         "departure_from",
#     ]
#     search_fields = [
#         "title",
#         "metaTitle",
#         "metaDescription",
#         "description",
#         "basePrice",
#         "cancellationPolicy",
#         "contactInformation",
#         "termsAndConditions",
#         "bookingInformation",
#     ]
#     ordering_fields = [
#         "createdAt",
#         "updatedAt",
#         "title",
#         "basePrice",
#         "duration",
#         "category",
#         "status",
#     ]
#     ordering = ["-createdAt"]
#     parser_classes = (MultiPartParser, FormParser)

#     def get_serializer_class(self):
#         if self.action in ["list"]:
#             return ProductSerializer
#         elif self.action in ["retrieve"]:
#             return ProductDetailSerializer
#         return ProductCreateUpdateSerializer

#     def create(self, request, *args, **kwargs):
#         with transaction.atomic():
#             return super().create(request, *args, **kwargs)

#     def update(self, request, *args, **kwargs):
#         with transaction.atomic():
#             return super().update(request, *args, **kwargs)

#     def partial_update(self, request, *args, **kwargs):
#         with transaction.atomic():
#             return super().partial_update(request, *args, **kwargs)


# class BookingViewSet(viewsets.ModelViewSet):
#     queryset = Booking.objects.all()
#     permission_classes = [IsAuthenticated]
#     pagination_class = BlogPagination
#     filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
#     filterset_fields = [
#         "user",
#         "api_category",
#         "status",
#     ]
#     search_fields = [
#         "product_title",
#         "user__email",
#         "user__first_name",
#         "duration",
#         "departure_from",
#         "location",
#     ]
#     ordering_fields = [
#         "product_title",
#         "user__email",
#         "title",
#         "total_amount",
#         "created_at",
#         "duration",
#         "status",
#     ]
#     ordering = ["-created_at"]

#     def get_serializer_class(self):
#         if self.action == "list":
#             return BookingListSerializer
#         elif self.action == "retrieve":
#             return BookingDetailSerializer
#         elif self.action in ["create", "update", "partial_update"]:
#             return BookingCreateUpdateSerializer
#         return BookingListSerializer

#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)

#     def perform_update(self, serializer):
#         serializer.save()


# def calculate_average(total, days):
#     return total / days if days > 0 else 0


# def calculate_percentage_difference(current_avg, all_time_avg):
#     if all_time_avg == 0:
#         return 100 if current_avg > 0 else 0
#     return ((current_avg - all_time_avg) / all_time_avg) * 100


# @api_view(["GET"])
# @permission_classes([IsAuthenticated])
# def dashboard_data(request, *args, **kwargs):
#     try:
#         # Get day parameter and calculate date range
#         day_param = int(request.query_params.get("day", "7"))
#         today = now()
#         start_date = today - timedelta(days=day_param)

#         # Aggregate data for all time
#         all_time_aggregates = Booking.objects.aggregate(
#             total_bookings=Count("id"),
#             total_sales=Sum("gross_amount"),
#             total_revenue=Sum("total_amount"),
#             total_cancellations=Count("id", filter=Q(status="Cancelled")),
#             first_booking_date=Min("created_at"),
#         )

#         # Aggregate data for the provided day range
#         provided_day_aggregates = Booking.objects.filter(
#             created_at__gte=start_date
#         ).aggregate(
#             total_bookings=Count("id"),
#             total_sales=Sum("gross_amount"),
#             total_revenue=Sum("total_amount"),
#             total_cancellations=Count("id", filter=Q(status="Cancelled")),
#         )

#         # Extract aggregated values
#         all_time_bookings = all_time_aggregates["total_bookings"]
#         all_time_sales = float(all_time_aggregates["total_sales"] or Decimal(0))
#         all_time_revenue = float(all_time_aggregates["total_revenue"] or Decimal(0))
#         all_time_cancellations = all_time_aggregates["total_cancellations"]

#         provided_day_bookings = provided_day_aggregates["total_bookings"]
#         provided_day_sales = float(provided_day_aggregates["total_sales"] or Decimal(0))
#         provided_day_revenue = float(
#             provided_day_aggregates["total_revenue"] or Decimal(0)
#         )
#         provided_day_cancellations = provided_day_aggregates["total_cancellations"]

#         # Calculate total days since the first booking
#         first_booking_date = all_time_aggregates["first_booking_date"]
#         total_days_since_first_booking = (
#             (today - first_booking_date).days if first_booking_date else 1
#         )

#         # Calculate averages
#         averages_all_time = {
#             "bookings": calculate_average(
#                 all_time_bookings, total_days_since_first_booking
#             ),
#             "sales": calculate_average(all_time_sales, total_days_since_first_booking),
#             "revenue": calculate_average(
#                 all_time_revenue, total_days_since_first_booking
#             ),
#             "cancellations": calculate_average(
#                 all_time_cancellations, total_days_since_first_booking
#             ),
#         }

#         averages_provided_days = {
#             "bookings": calculate_average(provided_day_bookings, day_param),
#             "sales": calculate_average(provided_day_sales, day_param),
#             "revenue": calculate_average(provided_day_revenue, day_param),
#             "cancellations": calculate_average(provided_day_cancellations, day_param),
#         }

#         # Calculate percentage differences
#         percentage_differences = {
#             "bookings": calculate_percentage_difference(
#                 averages_provided_days["bookings"], averages_all_time["bookings"]
#             ),
#             "sales": calculate_percentage_difference(
#                 averages_provided_days["sales"], averages_all_time["sales"]
#             ),
#             "revenue": calculate_percentage_difference(
#                 averages_provided_days["revenue"], averages_all_time["revenue"]
#             ),
#             "cancellations": calculate_percentage_difference(
#                 averages_provided_days["cancellations"],
#                 averages_all_time["cancellations"],
#             ),
#         }

#         recent_bookings = Booking.objects.order_by("-created_at")[:10]
#         recent_bookings_serializer = BookingListSerializer(recent_bookings, many=True)

#         data = {
#             "total_bookings": all_time_bookings,
#             "bookings_for_provided_days": provided_day_bookings,
#             "average_bookings_all_time_per_day": round(
#                 averages_all_time["bookings"], 2
#             ),
#             "average_bookings_provided_day_per_day": round(
#                 averages_provided_days["bookings"], 2
#             ),
#             "bookings_percent_difference": f"{percentage_differences['bookings']:+.2f}%",
#             "total_sales": f"${all_time_sales:,.2f}",
#             "sales_for_provided_days": f"${provided_day_sales:,.2f}",
#             "average_sales_all_time_per_day": f"${averages_all_time['sales']:,.2f}",
#             "average_sales_provided_day_per_day": f"${averages_provided_days['sales']:,.2f}",
#             "sales_percent_difference": f"{percentage_differences['sales']:+.2f}%",
#             "total_revenue": f"${all_time_revenue:,.2f}",
#             "revenue_for_provided_days": f"${provided_day_revenue:,.2f}",
#             "average_revenue_all_time_per_day": f"${averages_all_time['revenue']:,.2f}",
#             "average_revenue_provided_day_per_day": f"${averages_provided_days['revenue']:,.2f}",
#             "revenue_percent_difference": f"{percentage_differences['revenue']:+.2f}%",
#             "total_cancellations": all_time_cancellations,
#             "cancellations_for_provided_days": provided_day_cancellations,
#             "average_cancellations_all_time_per_day": round(
#                 averages_all_time["cancellations"], 2
#             ),
#             "average_cancellations_provided_day_per_day": round(
#                 averages_provided_days["cancellations"], 2
#             ),
#             "cancellations_percent_difference": f"{percentage_differences['cancellations']:+.2f}%",
#             "recent_bookings": recent_bookings_serializer.data,
#         }

#         return Response(
#             {"success": True, "message": "Dashboard data retrieved", "data": data},
#             status=status.HTTP_200_OK,
#         )

#     except Exception as e:
#         return Response(
#             {"error": "Internal Server Error", "details": str(e)},
#             status=status.HTTP_500_INTERNAL_SERVER_ERROR,
#         )
