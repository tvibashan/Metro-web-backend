from collections import defaultdict
from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

from users.models import User
from datetime import datetime, timedelta

API_CATEGORY_CHOICES = [
    ("G", "GLT"),
]

DISCOUNT_TYPE_CHOICES = [
    ("percentage", "Percentage"),
    # ('amount', 'Amount'),
]


class Day(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self) -> str:
        return self.name


# class DiscountForm(models.Model):
#     discount_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
#     discount_value = models.DecimalField(max_digits=10, decimal_places=2)
#     api_category = models.CharField(max_length=20, choices=API_CATEGORY_CHOICES)

#     def calculate_discount(self, original_price):
#         try:
#             discount_value = float(self.discount_value)
#         except ValueError:
#             return float(0)

#         if self.discount_type == "percentage":
#             discount = float(discount_value / 100) * float(original_price)
#             return discount
#         elif self.discount_type == "amount":
#             return float(discount_value)
#         else:
#             return float(0)

#     class Meta:
#         unique_together = ["api_category"]

#     def __str__(self):
#         return f"{self.discount_value} - {self.get_discount_type_display()} - {self.api_category}"


# class RetailPrice(models.Model):
#     DISCOUNT_TYPE_CHOICES = [
#         ("percentage", "Percentage"),
#         ("amount", "Amount"),
#     ]

#     increase_type = models.CharField(max_length=20, choices=DISCOUNT_TYPE_CHOICES)
#     increase_value = models.DecimalField(max_digits=10, decimal_places=2)
#     api_category = models.CharField(max_length=20, choices=API_CATEGORY_CHOICES)

#     def calculate_retail(self, original_price):
#         try:
#             increase_value = float(self.increase_value)
#         except ValueError:
#             return float(0)

#         if self.increase_type == "percentage":
#             increase = float(increase_value / 100) * float(original_price)
#         elif self.increase_type == "amount":
#             increase = float(increase_value)
#         else:
#             increase = float(0)

#         return float(original_price) + float(increase)

#     def __str__(self):
#         return f"{self.increase_value} - {self.get_increase_type_display()} - {self.api_category}"


class Option(models.Model):
    DROP_OFF_SAME_PLACE = "same_place"
    DROP_OFF_DIFFERENT_PLACE = "different_place"
    DROP_OFF_NO_SERVICE = "no_service"
    DROP_OFF_CHOICES = [
        (DROP_OFF_SAME_PLACE, "At the same place you meet them"),
        (DROP_OFF_DIFFERENT_PLACE, "At a different place"),
        (
            DROP_OFF_NO_SERVICE,
            "No drop-off service, the customer stays at the site or destination",
        ),
    ]
    name = models.CharField(max_length=100)
    reference_code = models.CharField(max_length=100, blank=True, null=True)
    maximum_group_size = models.IntegerField(default=2)
    is_wheelchair_accessible = models.BooleanField(default=False)
    skip_the_line = models.BooleanField(default=False)
    valid_for = models.IntegerField(default=1)
    has_fixed_time = models.BooleanField(default=False)
    audio_guide = models.BooleanField(default=False)
    booklet = models.BooleanField(default=False)
    is_private = models.BooleanField(default=False)
    drop_off_type = models.CharField(
        max_length=20,
        choices=DROP_OFF_CHOICES,
        default=DROP_OFF_SAME_PLACE,
        help_text="Specify the drop-off type for this option.",
    )
    MEETING_POINT_SET = "set_meeting_point"
    MEETING_POINT_CHOOSE = "choose_meeting_point"
    MEETING_POINT_CHOICES = [
        (MEETING_POINT_SET, "They go to a set meeting point"),
        (
            MEETING_POINT_CHOOSE,
            "They can choose where you pick them up from certain areas or a list of places",
        ),
    ]
    meeting_point_type = models.CharField(
        max_length=20,
        choices=MEETING_POINT_CHOICES,
        default=MEETING_POINT_SET,
        help_text="Specify how the meeting point is determined.",
    )


class Product(models.Model):
    languageType = models.CharField(max_length=100, null=True, blank=True)
    category = models.CharField(max_length=100, null=True, blank=True)
    title = models.CharField(max_length=255)
    metaTitle = models.CharField(max_length=255)
    metaDescription = models.TextField(null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    basePrice = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    basePriceFor = models.CharField(max_length=255, null=True, blank=True)
    departure_from = models.CharField(max_length=255, null=True, blank=True)
    duration = models.CharField(max_length=255)
    contactInformation = models.TextField(null=True, blank=True)
    bookingInformation = models.TextField(null=True, blank=True)
    termsAndConditions = models.TextField(null=True, blank=True)
    cancellationPolicy = models.TextField(null=True, blank=True)
    discount_percent = models.IntegerField(default=0)
    option = models.ForeignKey(
        Option,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="products",
    )
    status = models.BooleanField(default=False)
    isFoodIncluded = models.BooleanField(default=False)
    isTransportIncluded = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.metaTitle

    def get_discounted_price(self):
        if self.discount_percent < 0 or self.discount_percent > 100:
            raise ValueError("Discount percentage must be between 0 and 100.")

        try:
            base_price = float(self.basePrice)
        except ValueError:
            raise ValueError("Invalid base price. Ensure it is a valid number.")

        discounted_price = base_price * (1 - self.discount_percent / 100)
        return discounted_price

    @staticmethod
    def check_availability(product_id, requested_date):
        requested_date = timezone.make_aware(
            datetime.strptime(requested_date, "%Y-%m-%d")
        )

        schedules = ProductSchedule.objects.filter(
            product_id=product_id, available_days__name=requested_date.strftime("%A")
        )

        schedule_availability = defaultdict(list)

        for schedule in schedules:
            bookings = Booking.objects.filter(
                product_id=product_id,
                departure_date_time__range=(
                    datetime.combine(requested_date.date(), schedule.start_time),
                    datetime.combine(requested_date.date(), schedule.end_time),
                ),
                status__in=["Confirmed", "Reserved"],
            )
            booked_capacity = defaultdict(int)
            for booking in bookings:
                slot_start_time = booking.departure_date_time.time()
                if booking.participants.exists():
                    booked_capacity[slot_start_time] += sum(
                        participant.quantity
                        for participant in booking.participants.all()
                    )
                else:
                    booked_capacity[slot_start_time] += 1

            prices = schedule.prices.all()

            current_time = schedule.start_time
            while current_time < schedule.end_time:
                slot_end_time = (
                    datetime.combine(requested_date.date(), current_time)
                    + timedelta(minutes=schedule.interval_mins)
                ).time()
                if slot_end_time > schedule.end_time:
                    slot_end_time = schedule.end_time

                total_capacity = (
                    prices.aggregate(total_capacity=models.Sum("capacity"))[
                        "total_capacity"
                    ]
                    or 0
                )
                current_booked_capacity = booked_capacity.get(current_time, 0)
                available_capacity = total_capacity - current_booked_capacity

                if available_capacity > 0:
                    slot_prices = [
                        {
                            "price_id": price.id,
                            "name": price.name,
                            "option": price.option,
                            "price": float(price.price),
                            "capacity": price.capacity,
                        }
                        for price in prices
                    ]

                    schedule_availability[schedule].append(
                        {
                            "start_time": current_time,
                            "prices": slot_prices,
                        }
                    )

                current_time = slot_end_time

        result = [
            {
                "schedule_id": schedule.id,
                "schedule_name": schedule.name,
                "start_time": schedule.start_time,
                "end_time": schedule.end_time,
                "interval_mins": schedule.interval_mins,
                "available_slots": slots,
            }
            for schedule, slots in schedule_availability.items()
        ]

        return result


class MeetingPoint(models.Model):
    address = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    option = models.OneToOneField(Option, on_delete=models.CASCADE, related_name="meet")

    def __str__(self):
        return self.address


class DropOff(models.Model):
    address = models.CharField(max_length=255)
    landmark = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    option = models.OneToOneField(Option, on_delete=models.CASCADE, related_name="drop")

    def __str__(self):
        return self.address


class HostLanguage(models.Model):
    keyword = models.CharField(max_length=255)
    option = models.ForeignKey(
        Option, on_delete=models.CASCADE, related_name="host_languages"
    )

    def __str__(self):
        return self.keyword


class AudioGuideLanguage(models.Model):
    keyword = models.CharField(max_length=255)
    option = models.ForeignKey(
        Option, on_delete=models.CASCADE, related_name="audio_guides_languages"
    )

    def __str__(self):
        return self.keyword


class BookletLanguage(models.Model):
    keyword = models.CharField(max_length=255)
    option = models.ForeignKey(
        Option, on_delete=models.CASCADE, related_name="booklet_languages"
    )

    def __str__(self):
        return self.keyword


class ProductSchedule(models.Model):
    name = models.CharField(max_length=255)
    start_time = models.TimeField()
    end_time = models.TimeField()
    interval_mins = models.PositiveIntegerField()
    available_days = models.ManyToManyField(Day, related_name="product_schedules")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="schedules"
    )

    def __str__(self) -> str:
        return self.name

    class Meta:
        verbose_name = "Product Schedule"
        verbose_name_plural = "Product Schedules"


class ProductPrice(models.Model):
    schedule = models.ForeignKey(
        ProductSchedule, on_delete=models.CASCADE, related_name="prices"
    )
    name = models.CharField(max_length=150)
    option = models.CharField(max_length=250)
    capacity = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.name} - {self.price}"

    def get_discounted_price(self):
        product = self.schedule.product
        discount_percent = product.discount_percent

        if discount_percent < 0 or discount_percent > 100:
            raise ValueError("Discount percentage must be between 0 and 100.")

        try:
            base_price = float(self.price)
        except ValueError:
            raise ValueError("Invalid base price. Ensure it is a valid number.")

        discounted_price = base_price * (1 - discount_percent / 100)
        return discounted_price


class Summarize(models.Model):
    summaryText = models.TextField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="summarize"
    )

    def __str__(self):
        return self.summaryText


class Location(models.Model):
    address = models.TextField()
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="location"
    )

    def __str__(self):
        return self.address


class Keyword(models.Model):
    keyword = models.CharField(max_length=255)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="productKeywords"
    )

    def __str__(self):
        return self.keyword


class Image(models.Model):
    image = models.ImageField(upload_to="images/tours")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )


class InclusionService(models.Model):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="inclusions"
    )

    def __str__(self):
        return self.name


class ExclusionService(models.Model):
    name = models.CharField(max_length=255)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="exclusions"
    )

    def __str__(self):
        return self.name


class EmergencyContact(models.Model):
    name = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="emergencyContacts"
    )

    def __str__(self):
        return self.name


class AttractionTicket(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="attractionTicket"
    )
    ticketType = models.CharField(max_length=255)
    ageRestrictions = models.CharField(max_length=255, null=True, blank=True)
    accessibility = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.ticketType


class Tour1(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="tour"
    )
    tourType = models.CharField(max_length=255)
    locationsCovered = models.TextField(null=True, blank=True)
    guideInformation = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.tourType


class OverviewCard1(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="overviewcards"
    )
    icon = models.TextField()
    backgroundColor = models.CharField(max_length=50)
    liteBg = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    subtitle = models.TextField()

    def __str__(self):
        return self.title


class CityCard(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="cityCard"
    )
    cardName = models.CharField(max_length=255)
    validFor = models.CharField(max_length=255)
    activationMethod = models.CharField(max_length=255)

    def __str__(self):
        return self.cardName


class HopOnHopOffTicket(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="hopOnHopOffTicket"
    )
    routeInformation = models.TextField(null=True, blank=True)
    ticketType = models.CharField(max_length=255)
    operatingHours = models.CharField(max_length=255)
    frequency = models.CharField(max_length=255)

    def __str__(self):
        return self.ticketType


class Transfer(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="transfer"
    )
    transferType = models.CharField(max_length=255)
    pickupLocation = models.CharField(max_length=255)
    dropoffLocation = models.CharField(max_length=255)
    vehicleType = models.CharField(max_length=255)
    luggageAllowance = models.CharField(max_length=255)

    def __str__(self):
        return self.transferType


class Rental(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="rental"
    )
    rentalItemName = models.CharField(max_length=255)
    rentalType = models.CharField(max_length=255)
    rentalPeriod = models.CharField(max_length=255)
    ageRequirement = models.CharField(max_length=255, null=True, blank=True)
    damagePolicy = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.rentalItemName


class OtherCategory(models.Model):
    product = models.OneToOneField(
        Product, on_delete=models.CASCADE, related_name="otherCategory"
    )
    categoryType = models.CharField(max_length=255)
    activityName = models.CharField(max_length=255)
    specialRequirements = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.activityName


class PickupDropoff(models.Model):
    pickup = models.CharField(max_length=255)
    dropoff = models.CharField(max_length=255)
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="pickupDropoffs",
        null=True,
        blank=True,
    )
    tour = models.ForeignKey(
        Tour1,
        on_delete=models.CASCADE,
        related_name="pickupDropoffPoints",
        null=True,
        blank=True,
    )
    hopOnHopOffTicket = models.ForeignKey(
        HopOnHopOffTicket,
        on_delete=models.CASCADE,
        related_name="pickupDropoffPoints",
        null=True,
        blank=True,
    )

    def __str__(self):
        return f"{self.pickup} - {self.dropoff}"


class RedemptionPoint(models.Model):
    location = models.CharField(max_length=255)
    cityCard = models.ForeignKey(
        CityCard, on_delete=models.CASCADE, related_name="redemptionPoints"
    )

    def __str__(self):
        return self.location


class NotSuitable(models.Model):
    condition = models.CharField(max_length=255)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="notSuitable"
    )

    def __str__(self):
        return self.condition


class NotAllowed(models.Model):
    restriction = models.CharField(max_length=255)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="notAllowed"
    )

    def __str__(self):
        return self.restriction


class MustCarryItem(models.Model):
    item = models.CharField(max_length=255)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="mustCarryItems"
    )

    def __str__(self):
        return self.item


# class Option(models.Model):
#     name = models.CharField(max_length=255)
#     product = models.ForeignKey(
#         Product, on_delete=models.CASCADE, related_name="options", null=True, blank=True
#     )

#     def __str__(self):
#         return self.name


class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wishlist")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.email}'s Wishlist"


class WishlistItem(models.Model):
    wishlist = models.ForeignKey(
        Wishlist, on_delete=models.CASCADE, related_name="wishitems"
    )
    api_category = models.CharField(max_length=20, choices=API_CATEGORY_CHOICES)
    product_id = models.CharField(max_length=255)
    product_title = models.CharField(max_length=255, blank=True, null=True)
    product_image = models.CharField(max_length=255, blank=True, null=True)
    product_duration = models.CharField(max_length=255, blank=True, null=True)
    product_location = models.CharField(max_length=255, blank=True, null=True)
    product_price = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_title} - {self.wishlist.user}"


class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    api_category = models.CharField(
        max_length=20, choices=API_CATEGORY_CHOICES, default="G"
    )
    product_id = models.CharField(max_length=255)
    product_title = models.CharField(max_length=255, blank=True, null=True)
    product_image = models.CharField(max_length=255, blank=True, null=True)
    product_duration = models.CharField(max_length=255, blank=True, null=True)
    product_location = models.CharField(max_length=255, blank=True, null=True)
    product_price = models.CharField(max_length=255, blank=True, null=True)
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.product_title} - {self.user}"


class Booking(models.Model):
    BOOKING_STATUS_CHOICES = [
        ("Reserved", "Reserved"),
        ("Confirmed", "Confirmed"),
        ("Cancelled", "Cancelled"),
    ]

    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=True, null=True, related_name="bookings"
    )
    product_id = models.CharField(max_length=100, blank=True, null=True)
    product_title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    duration = models.CharField(max_length=255, blank=True, null=True)
    departure_from = models.CharField(max_length=255, blank=True, null=True)
    departure_date_time = models.DateTimeField(blank=True, null=True)
    product_thumbnail = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    gross_amount = models.DecimalField(max_digits=10, decimal_places=2)
    discount_percent = models.IntegerField(default=0)
    location = models.CharField(max_length=255, blank=True, null=True)

    qr_code = models.ImageField(upload_to="images/qr_code/", null=True, blank=True)
    api_category = models.CharField(max_length=20, choices=API_CATEGORY_CHOICES)

    status = models.CharField(
        max_length=20, choices=BOOKING_STATUS_CHOICES, default="Reserved"
    )

    is_valid = models.BooleanField(default=False)
    ticket_checker = models.CharField(max_length=255, blank=True, null=True)

    updated_at = models.DateTimeField(auto_now=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        user_email = getattr(self.user, "email", "N/A")
        return f"{user_email} - {self.product_title}"


class Participant(models.Model):
    booking = models.ForeignKey(
        Booking, on_delete=models.CASCADE, related_name="participants"
    )
    participant_type = models.CharField(max_length=10)
    quantity = models.PositiveIntegerField()
    cost_per_unit = models.DecimalField(max_digits=10, decimal_places=3)
    ticket = models.TextField(blank=True, null=True)
    ticket_info = models.TextField(blank=True, null=True)
    option_name = models.CharField(max_length=255, blank=True, null=True)

    def total_cost(self):
        return self.quantity * self.cost_per_unit
