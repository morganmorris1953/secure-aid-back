from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth.models import Group

# ========================================================
## Serializes user Model (simple_JWT)
# ========================================================
class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["name"] = user.username
        token["user_id"] = user.id

        recipient_group = user.groups.filter(name="Recipient").exists()
        veteran_group = user.groups.filter(name="Veteran").exists()

        if recipient_group:
            token["group"] = "recipient"

        elif veteran_group:
            token["group"] = "veteran"

        else:
            raise Exception("User must be in a group.")

        return token


class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer
