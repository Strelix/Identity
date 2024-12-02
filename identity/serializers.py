from rest_framework import serializers
from .models import User, Organization


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "email", "first_name", "last_name", "role", "is_active"]


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = ["id", "name", "leader", "members"]

    def validate_leader(self, value):
        """
        Ensure the leader exists in the user database.
        """
        if not User.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("The specified leader does not exist.")
        return value

    def create(self, validated_data):
        """
        Custom creation logic for organizations.
        """
        members = validated_data.pop("members", [])
        organization = Organization.objects.create(**validated_data)
        organization.members.set(members)
        return organization