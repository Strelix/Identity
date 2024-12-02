import requests
import json
from requests.exceptions import HTTPError

class IdentityClient:
    def __init__(self, base_url: str, api_key: str = None):
        self.base_url = base_url.rstrip("/")
        self.headers = {"Content-Type": "application/json"}
        if api_key:
            self.headers["Authorization"] = f"Bearer {api_key}"

    def request(self, method: str, path: str, data: dict = None, params: dict = None):
        """
        Centralized method to handle requests to the Identity service.
        """
        url = f"{self.base_url}/{path.lstrip('/')}"
        try:
            response = requests.request(
                method=method,
                url=url,
                headers=self.headers,
                json=data,
                params=params,
            )
            response.raise_for_status()
            return response.json()
        except HTTPError as e:
            # Optionally add detailed logging or re-raise the error
            return {"success": False, "error": str(e), "status_code": response.status_code}

    def verify_user_password(self, email: str, password: str):
        """
        Verifies user credentials with the Identity service.
        """
        return self.request(
            method="POST",
            path="/auth/verify-password/",
            data={"email": email, "password": password},
        )

    def get_user_by_id(self, user_id: int):
        """
        Fetches user details by ID.
        """
        return self.request(
            method="GET",
            path=f"/users/{user_id}/",
        )