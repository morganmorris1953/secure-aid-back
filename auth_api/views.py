from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import Group
from django.http import HttpResponseBadRequest

# ========================================================
## Serializes user Model (simple_JWT)
# ========================================================
class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["id"] = user.id
        token["username"] = user.username
        token["first_name"] = user.first_name
        token["last_name"] = user.last_name
        token["email"] = user.email

        groups = list(user.groups.values("id", "name"))

        if len(groups) != 1:
            raise Exception("User must be in a group.")

        token["group"] = groups.pop()

        return token


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer
