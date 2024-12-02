from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from identity.models import User, Organization

print("is USING HAHDFAHSHDAJHDHJI ADHJI AJNKDJKNAJKND AD ")

# from django.contrib.auth.models imp/ort User
# admin.register(Invoice)
admin.site.register(
    [
        Organization
    ]
)

fields = list(UserAdmin.fieldsets)  # type: ignore[arg-type]
fields[0] = (
    None,
    {
        "fields": (
            "username",
            "password",
            "logged_in_as_team",
            "awaiting_email_verification",
            "stripe_customer_id",
            "entitlements",
            "require_change_password",
        )
    },
)
UserAdmin.fieldsets = tuple(fields)
admin.site.register(User, UserAdmin)

admin.site.site_header = "Strelix Identity"
admin.site.index_title = "Strelix Identity"
admin.site.site_title = "Strelix | Identity Administration"
