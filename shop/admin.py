from django.contrib import admin

from .models import (
    Day,
    Product,
    ProductSchedule,
    ProductPrice,
    Review,
    Summarize,
    Location,
    Keyword,
    Image,
    InclusionService,
    ExclusionService,
    EmergencyContact,
    CityCard,
    MeetingPoint,
    DropOff,
    OverviewCard1,
    RedemptionPoint,
    Option,
    NotSuitable,
    NotAllowed,
    MustCarryItem,
    Wishlist,
    WishlistItem,
    Booking,
    Participant,
)

admin.site.register(DropOff)  
admin.site.register(MeetingPoint) 
admin.site.register(Option) 
admin.site.register(Day)


class ParticipantInline(admin.TabularInline):
    model = Participant


class WishlistItemInline(admin.TabularInline):
    model = WishlistItem


class BookingAdmin(admin.ModelAdmin):
    inlines = [ParticipantInline]


class BookingsAdmin(admin.ModelAdmin):
    search_fields = ("location", "product_title", "user__email")
    list_filter = ("location",)
    list_display = [
        "id",
        "user",
        "api_category",
        "product_title",
        "booking_id",
        "total_amount",
        "is_paid",
        "is_confirmed",
        "departure_date_time",
        "location",
    ]


admin.site.register(Booking, BookingAdmin)


class WishlistAdmin(admin.ModelAdmin):
    search_fields = ("user__email",)
    list_display = ["id", "user_email", "get_api_category"]
    inlines = [WishlistItemInline]

    def user_email(self, obj):
        return obj.user.email

    def get_api_category(self, obj):
        return ", ".join([item.api_category for item in obj.wishitems.all()])

    def get_product_title(self, obj):
        return ", ".join([item.product_title for item in obj.wishitems.all()])


admin.site.register(Wishlist, WishlistAdmin)


class WishlistItemAdmin(admin.ModelAdmin):
    search_fields = ("wishlist__user__email",)
    list_display = ["id", "get_user_email", "api_category", "get_title"]

    def get_user_email(self, obj):
        return obj.wishlist.user.email

    def get_title(self, obj):
        return obj.product_title

    get_user_email.short_description = "User Email"
    get_title.short_description = "Wished Product"


admin.site.register(WishlistItem, WishlistItemAdmin)
admin.site.register(Review)


# ------------------------------------------


class OverviewCard1Inline(admin.TabularInline):
    model = OverviewCard1
    extra = 1


class ProductScheduleInline(admin.TabularInline):
    model = ProductSchedule
    extra = 1


class SummarizeInline(admin.TabularInline):
    model = Summarize
    extra = 1


class LocationInline(admin.TabularInline):
    model = Location
    extra = 1


class KeywordInline(admin.TabularInline):
    model = Keyword
    extra = 1


class ImageInline(admin.TabularInline):
    model = Image
    extra = 1


class InclusionServiceInline(admin.TabularInline):
    model = InclusionService
    extra = 1


class ExclusionServiceInline(admin.TabularInline):
    model = ExclusionService
    extra = 1


class EmergencyContactInline(admin.TabularInline):
    model = EmergencyContact
    extra = 1


class NotSuitableInline(admin.TabularInline):
    model = NotSuitable
    extra = 1


class NotAllowedInline(admin.TabularInline):
    model = NotAllowed
    extra = 1


class MustCarryItemInline(admin.TabularInline):
    model = MustCarryItem
    extra = 1


# Admin for Product
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductScheduleInline,
        SummarizeInline,
        LocationInline,
        KeywordInline,
        ImageInline,
        InclusionServiceInline,
        ExclusionServiceInline,
        EmergencyContactInline,
        NotSuitableInline,
        NotAllowedInline,
        MustCarryItemInline,
        OverviewCard1Inline,
    ]


# Admin for ProductSchedule
class ProductPriceInline(admin.TabularInline):
    model = ProductPrice
    extra = 1


@admin.register(ProductSchedule)
class ProductScheduleAdmin(admin.ModelAdmin):
    inlines = [ProductPriceInline]


# Admin for CityCard
class RedemptionPointInline(admin.TabularInline):
    model = RedemptionPoint
    extra = 1


@admin.register(CityCard)
class CityCardAdmin(admin.ModelAdmin):
    inlines = [RedemptionPointInline]
