from datetime import datetime
from decimal import Decimal
from django.db import transaction, IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from blog.models import Blog, Reel
from blog.serializers import BlogListSerializer, ReelSerializer
from users.models import User
from shop.serializers import (
    GetBookingSerializer,
    ProductDetailSerializer,
    ProductSerializer,
)
from shop.models import Booking, Participant, Product, ProductPrice, Review
from django.db.models import OuterRef, Subquery


class GltAPI:
    @staticmethod
    def get_tours(request=None):
        product = Product.objects.all()
        tour_serializer = ProductSerializer(
            product, many=True, context={"request": request}
        )
        return tour_serializer.data

    @staticmethod
    def get_reels(request=None):
        reel = Reel.objects.all().order_by("created_at")[:4]
        reel_serializer = ReelSerializer(reel, many=True, context={"request": request})
        return reel_serializer.data

    @staticmethod
    def get_blogs(request=None):
        blog = Blog.objects.all().order_by("-created_at")[:4]
        blog_serializer = BlogListSerializer(
            blog, many=True, context={"request": request}
        )
        return blog_serializer.data

    @staticmethod
    def get_popular_products():
        latest_reviews = Review.objects.filter(
            product_id=OuterRef("pk"), rating__gt=2
        ).order_by("-created_at")

        products = (
            Product.objects.annotate(
                latest_review=Subquery(latest_reviews.values("created_at")[:1])
            )
            .filter(latest_review__isnull=False)
            .order_by("-latest_review")[:8]
        )

        product_serializer = ProductSerializer(products, many=True)
        return product_serializer.data + product_serializer.data

    @staticmethod
    def get_tour_detail(id, request=None):
        products = Product.objects.get(id=id)
        tour_serializer = ProductDetailSerializer(products, context={"request": request})
        return tour_serializer.data

    @staticmethod
    def check_availability(api_type, id, data=None):
        if api_type.upper() == "G":
            availability = Product.check_availability(id, data["requested_date"])
            return availability
        else:
            return {"error": "Invalid API Type"}

    @staticmethod
    def create_booking(data):
        required_fields = [
            "product_id",
            "user_id",
            "departure_date",
            "start_time",
            "items",
        ]

        for field in required_fields:
            if field not in data:
                raise ValueError(f"Missing required field: {field}")

        try:
            with transaction.atomic():
                tour = Product.objects.get(id=data["product_id"])
                discount_percent = tour.discount_percent

                departure_date = datetime.strptime(
                    data["departure_date"], "%Y-%m-%d"
                ).date()
                start_time = datetime.strptime(data["start_time"], "%H:%M:%S").time()
                departure_date_time = datetime.combine(departure_date, start_time)

                price_ids = [item["price_id"] for item in data["items"]]
                price_options = ProductPrice.objects.filter(id__in=price_ids)
                price_lookup = {str(price.id): price for price in price_options}

                for item in data["items"]:
                    if str(item["price_id"]) not in price_lookup:
                        raise ValueError(f"Invalid price ID: {item['price_id']}")

                booking = Booking.objects.create(
                    user=User.objects.get(id=data["user_id"]),
                    product_id=data["product_id"],
                    product_title=tour.title,
                    duration=tour.duration,
                    departure_from=tour.departure_from,
                    departure_date_time=departure_date_time,
                    product_thumbnail=data.get("image", ""),
                    total_amount=0,
                    gross_amount=0,
                    discount_percent=discount_percent,
                    api_category="G",
                    status="Reserved",
                )

                gross_amount = 0
                total_amount = 0

                for item in data["items"]:
                    price = price_lookup[str(item["price_id"])]
                    total_cost = price.price * item["quantity"]
                    gross_amount += total_cost

                    Participant.objects.create(
                        booking=booking,
                        participant_type=price.name,
                        option_name=price.option,
                        quantity=item["quantity"],
                        cost_per_unit=price.price,
                    )

                if discount_percent < 0 or discount_percent > 100:
                    raise ValueError("Discount percentage must be between 0 and 100.")

                total_amount = Decimal(gross_amount) * (
                    Decimal(1) - Decimal(discount_percent) / Decimal(100)
                )

                booking.gross_amount = gross_amount
                booking.total_amount = total_amount
                booking.save()

                booking_serializer = GetBookingSerializer(booking)
                serialized_data = booking_serializer.data

                return serialized_data

        except ObjectDoesNotExist as e:
            raise ValueError(f"Invalid reference: {e}")
        except IntegrityError as e:
            raise ValueError(f"Database error: {e}")
        except Exception as e:
            raise ValueError(f"An unexpected error occurred: {e}")

    @staticmethod
    def update_detail_booking(booking_id):
        booking = Booking.objects.get(id=booking_id)
        booking.status = "Confirmed"
        booking.save()

        # qr_image = qrcode.make(booking.booking_id)
        # file_name = f"{booking.user.email}-{booking.booking_id}-qr.png"
        # stream = BytesIO()
        # qr_image.save(stream, "PNG")
        # booking.qr_code.save(file_name, File(stream), save=True)

        # phone=str(booking.user.user_profile.phone)
        # sendVoucherMail(booking)
        # send_sms(phone,f'Your Cuore Tours {booking.product_title} Booking has been confirmed,  Your order id is {booking.booking_id} and type Glt, Collect your ticket from ticket counter')
        booking_serializer = GetBookingSerializer(booking)
        serialized_data = booking_serializer.data

        return serialized_data

    @staticmethod
    def get_detail_booking(booking_id):
        tours = Booking.objects.get(id=booking_id)
        tour_serializer = GetBookingSerializer(tours)
        return tour_serializer.data
