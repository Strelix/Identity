from rest_framework import serializers
from .models import User, Organization

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'role', 'entitlements', 'stripe_customer_id', 'logged_in_as_team', 'awaiting_email_verification']

class OrganizationSerializer(serializers.ModelSerializer):
    leader = UserSerializer()  # Include leader information in the response

    class Meta:
        model = Organization
        fields = ['id', 'name', 'leader', 'members', 'stripe_customer_id', 'entitlements']

class UserDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'is_active', 'role', 'entitlements', 'stripe_customer_id', 'logged_in_as_team', 'awaiting_email_verification', 'require_change_password']
