from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer

User = get_user_model()


class TeacherSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['id',
                  'first_name',
                  'last_name',
                  'email',
                  'job',
                  'profile_picture',
                  'password',
                  ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def to_representation(self, instance):
        # Get the original representation from the parent class
        representation = super().to_representation(instance)

        # Remove fields you don't want to include in the response
        representation['is_superuser'] = instance.is_superuser
        representation['is_staff'] = instance.is_staff

        return representation


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        token['id'] = f'{user.id}'
        token['firstName'] = user.first_name
        token['lastName'] = user.last_name
        token['email'] = user.email
        token['status'] = user.job
        token['profileImage'] = user.profile_picture.url if user.profile_picture else ''

        # del token['user_id']

        return token
