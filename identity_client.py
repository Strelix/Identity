import requests
import json
from requests.exceptions import HTTPError


class IdentityClient:
    def __init__(self, base_url: str, api_key: str = None, session_token: str = None):
        self.base_url = base_url
        self.api_key = api_key
        self.session_token = session_token
        self.session = requests.Session()
        self.session.headers.update({'Content-Type': 'application/json'})

        self.session.headers.update({'Authorization': f'Bearer {session_token or api_key}'})

    def authenticate(self, username: str, password: str):
        """
        Authenticate user and set session token.
        """
        auth_url = f"{self.base_url}/auth/token/"
        data = {
            "username": username,
            "password": password
        }
        try:
            response = self.session.post(auth_url, json=data)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx or 5xx)

            # Extract token from response
            token_data = response.json()
            self.session_token = token_data.get("access_token")
            self.session.headers.update({'Authorization': f'Bearer {self.session_token}'})
            return self.session_token
        except HTTPError as e:
            print(f"Authentication failed: {e}")
            return None

    def get_user(self, user_id: int):
        """
        Fetch user details by user ID.
        """
        url = f"{self.base_url}/users/{user_id}/"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            print(f"Error fetching user: {e}")
            return None

    def create_user(self, user_data: dict):
        """
        Create a new user.
        """
        url = f"{self.base_url}/users/"
        try:
            response = self.session.post(url, json=user_data)
            response.raise_for_status()
            return response.json()  # return created user data
        except HTTPError as e:
            print(f"Error creating user: {e}")
            return None

    def update_user(self, user_id: int, user_data: dict):
        """
        Update existing user by user ID.
        """
        url = f"{self.base_url}/users/{user_id}/"
        try:
            response = self.session.patch(url, json=user_data)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            print(f"Error updating user: {e}")
            return None

    def get_organizations(self):
        """
        Fetch all organizations.
        """
        url = f"{self.base_url}/organizations/"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            print(f"Error fetching organizations: {e}")
            return None

    def get_organization(self, org_id: int):
        """
        Fetch organization by ID.
        """
        url = f"{self.base_url}/organizations/{org_id}/"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            print(f"Error fetching organization: {e}")
            return None
