from django.urls import path
from identity import views
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),

    # User-related endpoints
    path("auth/verify-password/", views.verify_user_password, name="verify_user_password"),
    path("users/<int:user_id>/", views.get_user_by_id, name="get_user_by_id"),
    path("users/create/", views.create_user, name="create_user"),

    # Organization-related endpoints
    path("organizations/", views.list_organizations, name="list_organizations"),
    path("organizations/<int:org_id>/", views.get_organization_by_id, name="get_organization_by_id"),
    path("organizations/create/", views.create_organization, name="create_organization"),
]
