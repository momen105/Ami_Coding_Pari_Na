from django.contrib.auth.password_validation import validate_password
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db.models import Q
from rest_framework import exceptions, serializers, validators
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from user import models


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    JWT Custom Token Claims Serializer
    """

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token["is_superuser"] = user.is_superuser
        token["is_staff"] = user.is_staff

        return token


class NewUserSerializer(serializers.ModelSerializer):
    """
    New User Registration Serializer
    """

    username = serializers.CharField(
        required=True, validators=[UnicodeUsernameValidator()]
    )

    password = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
        required=True,
        validators=[validate_password],
    )
    password2 = serializers.CharField(
        style={"input_type": "password"},
        write_only=True,
        required=True,
        label="Retype Password",
    )
    restaurant = serializers.CharField(required=False)

    class Meta:
        model = models.User
        fields = ["username", "password", "password2", "restaurant"]

    def validate(self, attrs):
        if attrs["password"] != attrs["password2"]:
            raise validators.ValidationError({"password": "Password Doesn't Match"})
        if models.User.objects.filter(username=attrs["username"]).exists():
            raise validators.ValidationError(
                {"username": "user with this User ID already exists."}
            )
        return attrs

    def create(self, validated_data):
        user = models.User.objects.create(username=validated_data["username"])
        user.set_password(validated_data["password"])
        user.save()
        return user


class SearchSerializer(serializers.ModelSerializer):

    """
    Search serializer class
    """

    class Meta:
        model = models.SearchModel
        fields = "__all__"
