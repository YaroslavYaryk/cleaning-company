from django.contrib import admin
from .core.admin import BaseAdmin
from django.utils.safestring import mark_safe
from .models import User

# Register your models here.
class UserAdmin(BaseAdmin):

    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "phone",
        "is_active",
        "admin",
    )  # that's will be displayed in django-admin
    list_display_links = (
        "first_name",
        "last_name",
    )  # this ones we can click like links
    search_fields = ("email", "first_name", "last_name", "phone")
    list_editable = ["is_active"]
    # inlines = [ProductImageAdmin]
    fields = (
        "email",
        "first_name",
        "last_name",
        "phone",
        "birthdate",
        "address",
        "personal_number",
        "account_number",
        "picture",
        "get_image",
        "is_active",
        "admin",
        "staff",
    )
    readonly_fields = ("get_image",)

    def get_image(self, obj):
        if obj.picture:
            return mark_safe(f"<img src='{obj.picture.url}'width=200px>")
        else:
            return "no image"

    get_image.short_description = "picture"


admin.site.register(User, UserAdmin)
