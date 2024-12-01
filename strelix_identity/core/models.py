from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager
from django.utils import timezone
import itertools

class CustomUserManager(UserManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
            .select_related("user_profile", "logged_in_as_team")
            .annotate(notification_count=models.Count("user_notifications"))
        )


class User(AbstractUser):
    objects: CustomUserManager = CustomUserManager()  # type: ignore

    logged_in_as_team = models.ForeignKey("Organization", on_delete=models.SET_NULL, null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=255, null=True, blank=True)
    entitlements = models.JSONField(null=True, blank=True, default=list)  # List of strings (e.g., ["invoices"])
    awaiting_email_verification = models.BooleanField(default=True)
    require_change_password = models.BooleanField(default=False)  # Does user need to change password upon next login

    class Role(models.TextChoices):
        DEV = "DEV", "Developer"
        STAFF = "STAFF", "Staff"
        USER = "USER", "User"
        TESTER = "TESTER", "Tester"

    role = models.CharField(max_length=10, choices=Role.choices, default=Role.USER)

    @property
    def name(self):
        return self.first_name

    @property
    def teams_apart_of(self):
        return set(itertools.chain(self.teams_joined.all(), self.teams_leader_of.all()))

    @property
    def is_org(self):
        return False


class Organization(models.Model):
    name = models.CharField(max_length=100, unique=True)
    leader = models.ForeignKey(User, on_delete=models.CASCADE, related_name="teams_leader_of")
    members = models.ManyToManyField(User, related_name="teams_joined")

    stripe_customer_id = models.CharField(max_length=255, null=True, blank=True)
    entitlements = models.JSONField(null=True, blank=True, default=list)  # List of strings (e.g., ["invoices"])

    def is_owner(self, user: User) -> bool:
        return self.leader == user

    def is_logged_in_as_team(self, request) -> bool:
        if isinstance(request.auth, User):
            return False

        if request.auth and request.auth.organization_id == self.id:
            return True
        return False

    @property
    def is_authenticated(self):
        return True

    @property
    def is_org(self):
        return True
