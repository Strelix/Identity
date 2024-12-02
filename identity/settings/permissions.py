from rest_framework_api_key.permissions import KeyParser, BaseHasAPIKey
from rest_framework_api_key.models import APIKey

class BearerKeyParser(KeyParser):
    keyword = "Bearer"

class HasAPIKey(BaseHasAPIKey):
    model = APIKey  # Or a custom model
    key_parser = BearerKeyParser()