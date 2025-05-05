import json
from rest_framework import serializers
from django.db.models import Sum
from django.db.models import Avg

from common.serializers.user import UserListSerializer

from .models import (
    AudioGuideLanguage,
    Booking,
    BookletLanguage,
    Day,
    DropOff,
    HostLanguage,
    MeetingPoint,
    Option,
    OverviewCard1,
    ProductPrice,
    ProductSchedule,
    Participant,
    Review,
    Wishlist,
    WishlistItem,
    Product,
    Summarize,
    Location,
    Keyword,
    Image,
    InclusionService,
    ExclusionService,
    EmergencyContact,
    AttractionTicket,
    Tour1,
    CityCard,
    HopOnHopOffTicket,
    Transfer,
    Rental,
    OtherCategory,
    PickupDropoff,
    RedemptionPoint,
    # Option,
    NotSuitable,
    NotAllowed,
    MustCarryItem,
)


class ParticipantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Participant
        fields = "__all__"


class GetBookingSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True)

    class Meta:
        model = Booking
        fields = "__all__"


class BookingListSerializer(serializers.ModelSerializer):
    total_persons = serializers.SerializerMethodField()

    class Meta:
        model = Booking
        fields = [
            "id",
            "user",
            "product_title",
            "product_id",
            "departure_date_time",
            "duration",
            "departure_from",
            "product_thumbnail",
            "total_amount",
            "location",
            "total_persons",
            "api_category",
            "status",
            "created_at",
        ]

    def get_total_persons(self, obj):
        return obj.participants.aggregate(total=Sum("quantity"))["total"] or 0


class BookingDetailSerializer(serializers.ModelSerializer):
    participants = ParticipantSerializer(many=True, read_only=True)
    user = UserListSerializer()

    class Meta:
        model = Booking
        fields = [
            "id",
            "user",
            "product_id",
            "product_title",
            "subtitle",
            "duration",
            "departure_from",
            "departure_date_time",
            "product_thumbnail",
            "total_amount",
            "location",
            "qr_code",
            "api_category",
            "status",
            "is_valid",
            "ticket_checker",
            "updated_at",
            "created_at",
            "participants",
        ]


class BookingCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = [
            "user",
            "product_id",
            "product_title",
            "subtitle",
            "duration",
            "departure_from",
            "departure_date_time",
            "product_thumbnail",
            "total_amount",
            "location",
            "api_category",
            "status",
            "ticket_checker",
            "is_valid",
        ]


class WishlistItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = WishlistItem
        fields = "__all__"


class WishlistSerializer(serializers.ModelSerializer):
    wishitems = WishlistItemSerializer(many=True)

    class Meta:
        model = Wishlist
        fields = "__all__"


class ReviewSerializer(serializers.ModelSerializer):
    user = UserListSerializer()

    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = [
            "id",
            "user",
            "product_id",
            "product_title",
            "product_image",
            "product_duration",
            "product_location",
            "product_price",
        ]


class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = "__all__"
        read_only_fields = [
            "id",
            "user",
        ]


# ----------------------------------------------------------------------------------------------------------------------------------------------------


class SummarizeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Summarize
        fields = ["id", "summaryText"]


class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = ["id", "address"]


class KeywordSerializer(serializers.ModelSerializer):
    class Meta:
        model = Keyword
        fields = ["id", "keyword"]


class OverviewCard1Serializer(serializers.ModelSerializer):
    class Meta:
        model = OverviewCard1
        fields = [
            "icon",
            "backgroundColor",
            "liteBg",
            "title",
            "subtitle",
        ]


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ["image"]


class InclusionServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = InclusionService
        fields = ["id", "name"]


class ExclusionServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExclusionService
        fields = ["id", "name"]


class EmergencyContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = EmergencyContact
        fields = ["id", "name", "phone"]


class AttractionTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttractionTicket
        fields = ["id", "ticketType", "ageRestrictions", "accessibility"]


class TourSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour1
        fields = ["id", "tourType", "locationsCovered", "guideInformation"]


class CityCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = CityCard
        fields = ["id", "cardName", "validFor", "activationMethod"]


class HopOnHopOffTicketSerializer(serializers.ModelSerializer):
    class Meta:
        model = HopOnHopOffTicket
        fields = ["id", "routeInformation", "ticketType", "operatingHours", "frequency"]


class TransferSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transfer
        fields = [
            "id",
            "transferType",
            "pickupLocation",
            "dropoffLocation",
            "vehicleType",
            "luggageAllowance",
        ]


class RentalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Rental
        fields = [
            "id",
            "rentalItemName",
            "rentalType",
            "rentalPeriod",
            "ageRequirement",
            "damagePolicy",
        ]


class OtherCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OtherCategory
        fields = ["id", "categoryType", "activityName", "specialRequirements"]


class PickupDropoffSerializer(serializers.ModelSerializer):
    class Meta:
        model = PickupDropoff
        fields = ["id", "pickup", "dropoff", "tour", "hopOnHopOffTicket"]


class RedemptionPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = RedemptionPoint
        fields = ["id", "location", "cityCard"]


# class OptionSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Option
#         fields = ["id", "name"]


class NotSuitableSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotSuitable
        fields = ["id", "condition"]


class NotAllowedSerializer(serializers.ModelSerializer):
    class Meta:
        model = NotAllowed
        fields = ["id", "restriction"]


class MustCarryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MustCarryItem
        fields = ["id", "item"]


class DaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Day
        fields = ["id", "name"]


class ProductPriceSerializer(serializers.ModelSerializer):
    discounted_price = serializers.SerializerMethodField()

    class Meta:
        model = ProductPrice
        fields = ["id", "name", "option", "capacity", "price", "discounted_price"]

    def get_discounted_price(self, obj):
        return obj.get_discounted_price()


class ProductScheduleSerializer(serializers.ModelSerializer):
    prices = ProductPriceSerializer(many=True, required=False)
    available_days = DaySerializer(many=True)

    class Meta:
        model = ProductSchedule
        fields = [
            "id",
            "name",
            "start_time",
            "end_time",
            "interval_mins",
            "available_days",
            "prices",
        ]


class ProductScheduleCreateSerializer(serializers.ModelSerializer):
    prices = ProductPriceSerializer(many=True, required=False)

    class Meta:
        model = ProductSchedule
        fields = [
            "id",
            "name",
            "start_time",
            "end_time",
            "interval_mins",
            "available_days",
            "prices",
        ]


class MeetingPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = MeetingPoint
        fields = ["address", "landmark", "description", "latitude", "longitude"]


class DropOffSerializer(serializers.ModelSerializer):
    class Meta:
        model = DropOff
        fields = ["address", "landmark", "description", "latitude", "longitude"]


class HostLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = HostLanguage
        fields = ["keyword"]


class AudioGuideLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AudioGuideLanguage
        fields = ["keyword"]


class BookletLanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookletLanguage
        fields = ["keyword"]


class OptionDetailSerializer(serializers.ModelSerializer):
    meet = MeetingPointSerializer(required=False)
    drop = MeetingPointSerializer(required=False)
    host_languages = HostLanguageSerializer(many=True, required=False)
    audio_guides_languages = AudioGuideLanguageSerializer(many=True, required=False)
    booklet_languages = BookletLanguageSerializer(many=True, required=False)

    class Meta:
        model = Option
        fields = "__all__"


class OptionListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Option
        fields = "__all__"


class OptionCreateUpdateSerializer(serializers.ModelSerializer):
    meet = MeetingPointSerializer(required=False)
    drop = MeetingPointSerializer(required=False)
    host_languages = HostLanguageSerializer(many=True, required=False)
    audio_guides_languages = AudioGuideLanguageSerializer(many=True, required=False)
    booklet_languages = BookletLanguageSerializer(many=True, required=False)

    class Meta:
        model = Option
        fields = "__all__"

    def create(self, validated_data):
        request = self.context.get("request")
        data = request.data

        meet_data = self._parse_json_field(data, "meet")
        drop_data = self._parse_json_field(data, "drop")
        host_languages_data = self._parse_json_field(data, "host_languages")
        audio_guides_languages_data = self._parse_json_field(
            data, "audio_guides_languages"
        )
        booklet_languages_data = self._parse_json_field(data, "booklet_languages")

        validated_data.pop("meet", None)
        validated_data.pop("drop", None)
        validated_data.pop("host_languages", None)
        validated_data.pop("audio_guides_languages", None)
        validated_data.pop("booklet_languages", None)

        option = Option.objects.create(**validated_data)

        if meet_data:
            MeetingPoint.objects.create(option=option, **meet_data)

        if drop_data:
            DropOff.objects.create(option=option, **drop_data)

        if host_languages_data:
            for item in host_languages_data:
                HostLanguage.objects.create(option=option, **item)

        if audio_guides_languages_data:
            for item in audio_guides_languages_data:
                AudioGuideLanguage.objects.create(option=option, **item)

        if booklet_languages_data:
            for item in booklet_languages_data:
                BookletLanguage.objects.create(option=option, **item)

        option.save()
        return option

    def update(self, instance, validated_data):
        request = self.context.get("request")
        data = request.data

        meet_data = self._parse_json_field(data, "meet")
        drop_data = self._parse_json_field(data, "drop")
        host_languages_data = self._parse_json_field(data, "host_languages")
        audio_guides_languages_data = self._parse_json_field(
            data, "audio_guides_languages"
        )
        booklet_languages_data = self._parse_json_field(data, "booklet_languages")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if meet_data:
            if hasattr(instance, "meet"):
                for attr, value in meet_data.items():
                    setattr(instance.meet, attr, value)
                instance.meet.save()
            else:
                MeetingPoint.objects.create(option=instance, **meet_data)

        if drop_data:
            if hasattr(instance, "drop"):
                for attr, value in drop_data.items():
                    setattr(instance.drop, attr, value)
                instance.drop.save()
            else:
                DropOff.objects.create(option=instance, **drop_data)

        if host_languages_data:
            instance.host_languages.all().delete()
            for item in host_languages_data:
                HostLanguage.objects.create(option=instance, **item)

        # Update or create AudioGuideLanguage
        if audio_guides_languages_data:
            instance.audio_guides_languages.all().delete()
            for item in audio_guides_languages_data:
                AudioGuideLanguage.objects.create(option=instance, **item)

        # Update or create BookletLanguage
        if booklet_languages_data:
            instance.booklet_languages.all().delete()
            for item in booklet_languages_data:
                BookletLanguage.objects.create(option=instance, **item)

        return instance

    def _parse_json_field(self, data, field_name):
        field_value = data.get(field_name, None)
        if field_value and isinstance(field_value, str):
            try:
                return json.loads(field_value)
            except json.JSONDecodeError:
                raise serializers.ValidationError({field_name: "Invalid JSON format."})
        return field_value


class ProductSerializer(serializers.ModelSerializer):
    location = LocationSerializer(many=True, required=False)
    images = ImageSerializer(many=True, required=False)
    discounted_base_price = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            "id",
            "title",
            "metaTitle",
            "basePrice",
            "basePriceFor",
            "location",
            "duration",
            "discount_percent",
            "status",
            "departure_from",
            "category",
            "images",
            "isFoodIncluded",
            "isTransportIncluded",
            "createdAt",
            "updatedAt",
            "discounted_base_price",
            "avg_rating",
            "total_reviews",
        ]

    def get_discounted_base_price(self, obj):
        return obj.get_discounted_price()

    def get_avg_rating(self, obj):
        avg_rating = Review.objects.filter(product_id=obj.id).aggregate(Avg("rating"))[
            "rating__avg"
        ]
        return round(avg_rating, 2) if avg_rating is not None else 0

    def get_total_reviews(self, obj):
        total_reviews = Review.objects.filter(product_id=obj.id).count()
        return total_reviews


class ProductDetailSerializer(serializers.ModelSerializer):
    summarize = SummarizeSerializer(many=True, required=False)
    location = LocationSerializer(many=True, required=False)
    productKeywords = KeywordSerializer(many=True, required=False)
    overviewcards = OverviewCard1Serializer(many=True, required=False)
    images = ImageSerializer(many=True, required=False)
    inclusions = InclusionServiceSerializer(many=True, required=False)
    exclusions = ExclusionServiceSerializer(many=True, required=False)
    emergencyContacts = EmergencyContactSerializer(many=True, required=False)
    attractionTicket = AttractionTicketSerializer(required=False)
    tour = TourSerializer(required=False)
    option = OptionDetailSerializer(required=False)
    cityCard = CityCardSerializer(required=False)
    hopOnHopOffTicket = HopOnHopOffTicketSerializer(required=False)
    transfer = TransferSerializer(required=False)
    rental = RentalSerializer(required=False)
    otherCategory = OtherCategorySerializer(required=False)
    pickupDropoffs = PickupDropoffSerializer(many=True, required=False)
    notSuitable = NotSuitableSerializer(many=True, required=False)
    notAllowed = NotAllowedSerializer(many=True, required=False)
    mustCarryItems = MustCarryItemSerializer(many=True, required=False)
    schedules = ProductScheduleSerializer(many=True, required=False)
    discounted_base_price = serializers.SerializerMethodField()
    avg_rating = serializers.SerializerMethodField()
    total_reviews = serializers.SerializerMethodField()

    def get_discounted_base_price(self, obj):
        return obj.get_discounted_price()

    def get_avg_rating(self, obj):
        avg_rating = Review.objects.filter(product_id=obj.id).aggregate(Avg("rating"))[
            "rating__avg"
        ]
        return round(avg_rating, 2) if avg_rating is not None else 0

    def get_total_reviews(self, obj):
        total_reviews = Review.objects.filter(product_id=obj.id).count()
        return total_reviews

    class Meta:
        model = Product
        fields = "__all__"


class ProductCreateUpdateSerializer(serializers.ModelSerializer):
    summarize = SummarizeSerializer(many=True, required=False)
    location = LocationSerializer(many=True, required=False)
    productKeywords = KeywordSerializer(many=True, required=False)
    overviewcards = OverviewCard1Serializer(many=True, required=False)
    inclusions = InclusionServiceSerializer(many=True, required=False)
    exclusions = ExclusionServiceSerializer(many=True, required=False)
    emergencyContacts = EmergencyContactSerializer(many=True, required=False)
    attractionTicket = AttractionTicketSerializer(required=False)
    tour = TourSerializer(required=False)
    cityCard = CityCardSerializer(required=False)
    hopOnHopOffTicket = HopOnHopOffTicketSerializer(required=False)
    transfer = TransferSerializer(required=False)
    rental = RentalSerializer(required=False)
    otherCategory = OtherCategorySerializer(required=False)
    pickupDropoffs = PickupDropoffSerializer(many=True, required=False)
    notSuitable = NotSuitableSerializer(many=True, required=False)
    notAllowed = NotAllowedSerializer(many=True, required=False)
    mustCarryItems = MustCarryItemSerializer(many=True, required=False)
    schedules = ProductScheduleCreateSerializer(many=True, required=False)
    images = ImageSerializer(many=True, required=False)

    class Meta:
        model = Product
        fields = [
            "id",
            "languageType",
            "title",
            "category",
            "metaTitle",
            "departure_from",
            "metaDescription",
            "description",
            "basePrice",
            "basePriceFor",
            "discount_percent",
            "cancellationPolicy",
            "duration",
            "option",
            "contactInformation",
            "termsAndConditions",
            "bookingInformation",
            "status",
            "isFoodIncluded",
            "isTransportIncluded",
            "createdAt",
            "updatedAt",
            "summarize",
            "location",
            "productKeywords",
            "overviewcards",
            "images",
            "inclusions",
            "exclusions",
            "emergencyContacts",
            "attractionTicket",
            "tour",
            "cityCard",
            "hopOnHopOffTicket",
            "transfer",
            "rental",
            "otherCategory",
            "pickupDropoffs",
            "notSuitable",
            "notAllowed",
            "mustCarryItems",
            "schedules",
        ]

    def _parse_json_field(self, data, field_name):
        field_value = data.get(field_name, None)
        if field_value and isinstance(field_value, str):
            try:
                return json.loads(field_value)
            except json.JSONDecodeError:
                raise serializers.ValidationError({field_name: "Invalid JSON format."})
        return field_value

    def create(self, validated_data):
        request = self.context.get("request")
        data = request.data

        city_card_data = self._parse_json_field(data, "cityCard")
        schedules_data = self._parse_json_field(data, "schedules")
        summarize_data = self._parse_json_field(data, "summarize")
        location_data = self._parse_json_field(data, "location")
        product_keywords_data = self._parse_json_field(data, "productKeywords")
        overviewcards_data = self._parse_json_field(data, "overviewcards")
        inclusions_data = self._parse_json_field(data, "inclusions")
        exclusions_data = self._parse_json_field(data, "exclusions")
        emergency_contacts_data = self._parse_json_field(data, "emergencyContacts")
        attraction_ticket_data = self._parse_json_field(data, "attractionTicket")
        tour_data = self._parse_json_field(data, "tour")
        hop_on_hop_off_ticket_data = self._parse_json_field(data, "hopOnHopOffTicket")
        transfer_data = self._parse_json_field(data, "transfer")
        rental_data = self._parse_json_field(data, "rental")
        other_category_data = self._parse_json_field(data, "otherCategory")
        pickup_dropoffs_data = self._parse_json_field(data, "pickupDropoffs")
        not_suitable_data = self._parse_json_field(data, "notSuitable")
        not_allowed_data = self._parse_json_field(data, "notAllowed")
        must_carry_items_data = self._parse_json_field(data, "mustCarryItems")

        validated_data.pop("cityCard", None)
        validated_data.pop("schedules", None)
        validated_data.pop("attractionTicket", None)
        validated_data.pop("tour", None)
        validated_data.pop("hopOnHopOffTicket", None)
        validated_data.pop("transfer", None)
        validated_data.pop("rental", None)
        validated_data.pop("otherCategory", None)
        validated_data.pop("pickupDropoffs", None)
        validated_data.pop("notSuitable", None)
        validated_data.pop("notAllowed", None)
        validated_data.pop("mustCarryItems", None)

        images_data = request.FILES.getlist("images")

        product = Product.objects.create(**validated_data)

        if city_card_data:
            CityCard.objects.create(product=product, **city_card_data)

        if schedules_data:
            for schedule_data in schedules_data:
                prices_data = schedule_data.pop("prices", [])
                available_days = schedule_data.pop("available_days", [])

                schedule = ProductSchedule.objects.create(
                    product=product, **schedule_data
                )

                if available_days:
                    schedule.available_days.set(available_days)

                for price_data in prices_data:
                    ProductPrice.objects.create(schedule=schedule, **price_data)

        if images_data:
            for image_file in images_data:
                Image.objects.create(product=product, image=image_file)

        if summarize_data:
            for item in summarize_data:
                Summarize.objects.create(product=product, **item)

        if location_data:
            for item in location_data:
                Location.objects.create(product=product, **item)

        if product_keywords_data:
            for item in product_keywords_data:
                Keyword.objects.create(product=product, **item)

        if overviewcards_data:
            for item in overviewcards_data:
                OverviewCard1.objects.create(product=product, **item)

        if inclusions_data:
            for item in inclusions_data:
                InclusionService.objects.create(product=product, **item)

        if exclusions_data:
            for item in exclusions_data:
                ExclusionService.objects.create(product=product, **item)

        if emergency_contacts_data:
            for item in emergency_contacts_data:
                EmergencyContact.objects.create(product=product, **item)

        if attraction_ticket_data:
            AttractionTicket.objects.create(product=product, **attraction_ticket_data)

        if tour_data:
            Tour1.objects.create(product=product, **tour_data)

        if hop_on_hop_off_ticket_data:
            HopOnHopOffTicket.objects.create(
                product=product, **hop_on_hop_off_ticket_data
            )

        if transfer_data:
            Transfer.objects.create(product=product, **transfer_data)

        if rental_data:
            Rental.objects.create(product=product, **rental_data)

        if other_category_data:
            OtherCategory.objects.create(product=product, **other_category_data)

        if pickup_dropoffs_data:
            for item in pickup_dropoffs_data:
                PickupDropoff.objects.create(product=product, **item)

        if not_suitable_data:
            for item in not_suitable_data:
                NotSuitable.objects.create(product=product, **item)

        if not_allowed_data:
            for item in not_allowed_data:
                NotAllowed.objects.create(product=product, **item)

        if must_carry_items_data:
            for item in must_carry_items_data:
                MustCarryItem.objects.create(product=product, **item)

        product.save()
        return product

    def update(self, instance, validated_data):
        request = self.context.get("request")
        data = request.data

        summarize_data = self._parse_json_field(validated_data, "summarize")
        location_data = self._parse_json_field(validated_data, "location")
        product_keywords_data = self._parse_json_field(
            validated_data, "productKeywords"
        )
        overviewcards_data = self._parse_json_field(validated_data, "overviewcards")
        inclusions_data = self._parse_json_field(validated_data, "inclusions")
        exclusions_data = self._parse_json_field(validated_data, "exclusions")
        emergency_contacts_data = self._parse_json_field(
            validated_data, "emergencyContacts"
        )
        attraction_ticket_data = self._parse_json_field(
            validated_data, "attractionTicket"
        )
        tour_data = self._parse_json_field(validated_data, "tour")
        city_card_data = self._parse_json_field(validated_data, "cityCard")
        hop_on_hop_off_ticket_data = self._parse_json_field(
            validated_data, "hopOnHopOffTicket"
        )
        transfer_data = self._parse_json_field(validated_data, "transfer")
        rental_data = self._parse_json_field(validated_data, "rental")
        other_category_data = self._parse_json_field(validated_data, "otherCategory")
        pickup_dropoffs_data = self._parse_json_field(validated_data, "pickupDropoffs")
        not_suitable_data = self._parse_json_field(validated_data, "notSuitable")
        not_allowed_data = self._parse_json_field(validated_data, "notAllowed")
        must_carry_items_data = self._parse_json_field(validated_data, "mustCarryItems")
        schedules_data = self._parse_json_field(validated_data, "schedules")

        validated_data.pop("images", None)
        validated_data.pop("summarize", None)
        validated_data.pop("location", None)
        validated_data.pop("productKeywords", None)
        validated_data.pop("overviewcards", None)
        validated_data.pop("inclusions", None)
        validated_data.pop("exclusions", None)
        validated_data.pop("emergencyContacts", None)
        validated_data.pop("attractionTicket", None)
        validated_data.pop("tour", None)
        validated_data.pop("cityCard", None)
        validated_data.pop("hopOnHopOffTicket", None)
        validated_data.pop("transfer", None)
        validated_data.pop("rental", None)
        validated_data.pop("otherCategory", None)
        validated_data.pop("pickupDropoffs", None)
        validated_data.pop("notSuitable", None)
        validated_data.pop("notAllowed", None)
        validated_data.pop("mustCarryItems", None)
        validated_data.pop("schedules", None)

        images_data = request.FILES.getlist("images")

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if summarize_data:
            instance.summarize.all().delete()
            for data in summarize_data:
                Summarize.objects.create(**data, product=instance)

        if location_data:
            instance.location.all().delete()
            for data in location_data:
                Location.objects.create(**data, product=instance)

        if product_keywords_data:
            instance.productKeywords.all().delete()
            for data in product_keywords_data:
                Keyword.objects.create(**data, product=instance)

        if overviewcards_data:
            instance.overviewcards.all().delete()
            for data in overviewcards_data:
                OverviewCard1.objects.create(**data, product=instance)

        if inclusions_data:
            instance.inclusions.all().delete()
            for data in inclusions_data:
                InclusionService.objects.create(**data, product=instance)

        if exclusions_data:
            instance.exclusions.all().delete()
            for data in exclusions_data:
                ExclusionService.objects.create(**data, product=instance)

        if emergency_contacts_data:
            instance.emergencyContacts.all().delete()
            for data in emergency_contacts_data:
                EmergencyContact.objects.create(**data, product=instance)

        if pickup_dropoffs_data:
            instance.pickupDropoffs.all().delete()
            for data in pickup_dropoffs_data:
                PickupDropoff.objects.create(**data, product=instance)

        if not_suitable_data:
            instance.notSuitable.all().delete()
            for data in not_suitable_data:
                NotSuitable.objects.create(**data, product=instance)

        if not_allowed_data:
            instance.notAllowed.all().delete()
            for data in not_allowed_data:
                NotAllowed.objects.create(**data, product=instance)

        if must_carry_items_data:
            instance.mustCarryItems.all().delete()
            for data in must_carry_items_data:
                MustCarryItem.objects.create(**data, product=instance)

        if attraction_ticket_data:
            if instance.attractionTicket:
                for attr, value in attraction_ticket_data.items():
                    setattr(instance.attractionTicket, attr, value)
                instance.attractionTicket.save()
            else:
                AttractionTicket.objects.create(
                    **attraction_ticket_data, product=instance
                )

        if tour_data:
            if instance.tour:
                for attr, value in tour_data.items():
                    setattr(instance.tour, attr, value)
                instance.tour.save()
            else:
                Tour1.objects.create(**tour_data, product=instance)

        if city_card_data:
            if instance.cityCard:
                for attr, value in city_card_data.items():
                    setattr(instance.cityCard, attr, value)
                instance.cityCard.save()
            else:
                CityCard.objects.create(**city_card_data, product=instance)

        if hop_on_hop_off_ticket_data:
            if instance.hopOnHopOffTicket:
                for attr, value in hop_on_hop_off_ticket_data.items():
                    setattr(instance.hopOnHopOffTicket, attr, value)
                instance.hopOnHopOffTicket.save()
            else:
                HopOnHopOffTicket.objects.create(
                    **hop_on_hop_off_ticket_data, product=instance
                )

        if transfer_data:
            if instance.transfer:
                for attr, value in transfer_data.items():
                    setattr(instance.transfer, attr, value)
                instance.transfer.save()
            else:
                Transfer.objects.create(**transfer_data, product=instance)

        if rental_data:
            if instance.rental:
                for attr, value in rental_data.items():
                    setattr(instance.rental, attr, value)
                instance.rental.save()
            else:
                Rental.objects.create(**rental_data, product=instance)

        if other_category_data:
            if instance.otherCategory:
                for attr, value in other_category_data.items():
                    setattr(instance.otherCategory, attr, value)
                instance.otherCategory.save()
            else:
                OtherCategory.objects.create(**other_category_data, product=instance)

        if schedules_data:
            instance.schedules.all().delete()
            for schedule_data in schedules_data:
                prices_data = schedule_data.pop("prices", [])
                available_days = schedule_data.pop("available_days", [])
                schedule = ProductSchedule.objects.create(
                    product=instance, **schedule_data
                )
                if available_days:
                    schedule.available_days.set(available_days)
                for price_data in prices_data:
                    ProductPrice.objects.create(schedule=schedule, **price_data)

        if images_data:
            instance.images.all().delete()
            for image in images_data:
                Image.objects.create(product=instance, **image)

        instance.save()

        return instance
