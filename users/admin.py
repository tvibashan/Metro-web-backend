from django.contrib import admin
from .models import (
    User,
)

admin.site.site_header = "CUORE TOURS SuperAdmin"
admin.site.site_title = "CUORE TOURS SuperAdmin Panel"


class UserAdmin(admin.ModelAdmin):
    list_display = ("email", "date_joined", "last_login", "display_groups")
    search_fields = (
        "email",
        "first_name",
        "last_name",
    )
    list_filter = ("is_staff", "is_active")
    fields = (
        "email",
        "first_name",
        "last_name",
        "password",
        "image",
        "phone",
        "date_of_birth",
        "address",
        "country",
        "city",
        "user_permissions",
        "is_superuser",
        "is_staff",
        "is_active",
    )

    def display_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])


admin.site.register(User, UserAdmin)
