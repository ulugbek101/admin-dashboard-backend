from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()


class TeacherSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'username', 'email', 'created', 'password']
        extra_kwargs = {
            'password': {
                'write_only': True,
                'style': {
                    'input_type': 'password'
                }
            },
            'username': {
                'read_only': True
            }
        }

    def create(self, validated_data):
        """ Create a new user instance with hashed password """

        password = validated_data.pop('password', None)
        first_name = validated_data.get('first_name').capitalize()
        last_name = validated_data.get('last_name').capitalize()
        validated_data['username'] = f'{first_name}{last_name}'
        user = super(TeacherSerializer, self).create(validated_data)

        if password:
            user.set_password(password)
            user.save()

        return user

    def update(self, instance, validated_data):
        """ Update and return existing user instance """

        password = validated_data.pop('password', None)
        user = super(TeacherSerializer, self).update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['email'] = user.email
        token['status'] = 'Superadmin' if user.is_superuser else 'Xodim'
        token['profile_image'] = user.profile_picture.url

        return token
