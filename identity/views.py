from django.contrib.auth import authenticate
from rest_framework.decorators import api_view
from rest_framework.request import Request
from .models import User, Organization
from .response import APIResponse
from .serializers import UserSerializer, OrganizationSerializer


@api_view(["POST"])
def verify_user_password(request: Request):
    """
    Verifies the user's email and password.
    """
    email = request.data.get("email")
    password = request.data.get("password")

    user = authenticate(request, username=email, password=password)

    if not user:
        return APIResponse(False, "Incorrect email or password", status=401)

    return APIResponse(
        True,
        {
            "user_id": user.id,  # type: ignore[attr-defined]
            "message": "Successfully authenticated user",
        },
        status=200,
    )


@api_view(["GET"])
def get_user_by_id(request: Request, user_id: int):
    """
    Fetches user details by ID.
    """
    try:
        user = User.objects.get(is_active=True, id=user_id)
    except User.DoesNotExist:
        return APIResponse(False, "User does not exist with that ID", status=404)

    serializer = UserSerializer(user)
    return APIResponse(True, serializer.data, status=200)


@api_view(["POST"])
def create_user(request):
    """
    Creates a new user in the system.
    """
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        return APIResponse(True, {"user_id": user.id, "message": "User created successfully"}, status=201)
    return APIResponse(False, serializer.errors, status=400)


@api_view(["GET"])
def list_organizations(request):
    """
    Returns a list of all organizations.
    """
    organizations = Organization.objects.all()
    serializer = OrganizationSerializer(organizations, many=True)
    return APIResponse(True, serializer.data, status=200)


@api_view(["GET"])
def get_organization_by_id(request, org_id):
    """
    Fetches an organization's details by ID.
    """
    try:
        organization = Organization.objects.get(id=org_id)
    except Organization.DoesNotExist:
        return APIResponse(False, "Organization does not exist", status=404)

    serializer = OrganizationSerializer(organization)
    return APIResponse(True, serializer.data, status=200)


@api_view(["POST"])
def create_organization(request):
    """
    Creates a new organization in the system.
    """
    serializer = OrganizationSerializer(data=request.data)
    if serializer.is_valid():
        organization = serializer.save()
        return APIResponse(True, {"organization_id": organization.id, "message": "Organization created successfully"}, status=201)
    return APIResponse(False, serializer.errors, status=400)
