from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.serializers import ModelSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Custom token obtain pair serializer to include additional user information in the token.

    This serializer extends Django Rest Framework's TokenObtainPairSerializer and adds custom claims
    such as email, username, full name, status, and profile image URL to the token.

    Attributes:
        None

    Methods:
        get_token(cls, user): Retrieves the token for the given user and adds custom claims to it,
            including email, username, full name, status, and profile image URL.

    """

    @classmethod
    def get_token(cls, user):
        """
        Retrieve the token for the given user and add custom claims.

        Args:
            user: The user for which to generate the token.

        Returns:
            Token with custom claims added.
        """

        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['full_name'] = user.get_full_name()
        token['status'] = user.status
        token['is_superuser'] = user.is_superuser
        token['is_admin'] = user.is_admin
        token['is_teacher'] = user.is_teacher
        token['profile_image'] = user.profile_image.url if user.profile_image else None

        return token


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        exclude = ['date_joined', 'last_login', 'is_active', 'is_staff', 'groups', 'user_permissions']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password',
                }
            }
        }

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['created'] = instance.date_joined
        representation['updated'] = instance.last_login
        return representation
