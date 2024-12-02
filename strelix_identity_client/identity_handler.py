from typing import Optional
from django.contrib.auth.models import User
from identity_client import IdentityClient


class UserHandler:
    def __init__(self, use_identity_service: bool = False, identity_creds: Optional[dict] = None, LocalUserModel=User):
        self.use_identity_service = use_identity_service
        self.identity_client = IdentityClient(identity_creds) if use_identity_service else None
        self.LocalUserModel = LocalUserModel

    def get_user_by_id(self, user_id: int):
        """
        Fetch user by ID, either from the local database or the Identity service.
        """
        if self.use_identity_service:
            return self.identity_client.get_user(user_id=user_id)
        return self.LocalUserModel.objects.filter(id=user_id).first()

    def authenticate_user(self, email: str, password: str):
        """
        Authenticate a user, using either the local DB or the Identity service.
        """
        if self.use_identity_service:
            return self.identity_client.verify_user_password(email=email, password=password)
        from django.contrib.auth import authenticate
        return authenticate(username=email, password=password)

    def create_user(self, **kwargs):
        """
        Create a new user in either the local database or the Identity service.
        """
        if self.use_identity_service:
            return self.identity_client.create_user(**kwargs)
        return self.LocalUserModel.objects.create_user(**kwargs)

    def list_users(self):
        """
        List all users, from either the local database or the Identity service.
        """
        if self.use_identity_service:
            return self.identity_client.list_users()
        return self.LocalUserModel.objects.all()