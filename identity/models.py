from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager, Group, Permission
from django.utils import timezone
import itertools

class CustomUserManager(UserManager):
    def get_queryset(self):
        return (
            super()
            .get_queryset()
        )


class User(AbstractUser):
    objects: CustomUserManager = CustomUserManager()  # type: ignore

    groups = models.ManyToManyField(
        Group,
        related_name="custom_user_set",  # Unique related name
        blank=True,
        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
        verbose_name="groups",
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name="custom_user_permissions_set",  # Unique related name
        blank=True,
        help_text="Specific permissions for this user.",
        verbose_name="user permissions",
    )

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
