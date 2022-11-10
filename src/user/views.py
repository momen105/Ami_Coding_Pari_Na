from rest_framework import generics, permissions, response, status
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView
from datetime import datetime
import locale
import json

# import helper
import helper

# from organization import models as organization_models
from user import models, serializers


class MyTokenObtainPairView(TokenObtainPairView):
    """
    JWT Custom Token Claims View
    """

    serializer_class = serializers.MyTokenObtainPairSerializer

    @staticmethod
    def token_helper(serializer, user):
        serializer.is_valid(raise_exception=True)
        otp = models.OTPModel.objects.get(user=user)
        if not otp.is_active:
            return response.Response(
                serializer.validated_data, status=status.HTTP_200_OK
            )
        refresh_token = RefreshToken.for_user(user)
        fer_key = helper.encode(str(refresh_token))
        return response.Response({"secret": fer_key}, status=status.HTTP_202_ACCEPTED)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        try:
            user = models.User.objects.get(username=request.data["username"])
            try:
                return self.token_helper(serializer, user)
            except TokenError as e:
                raise InvalidToken(e.args[0]) from e
        except Exception as e:
            serializer.is_valid(raise_exception=True)
            return response.Response(
                serializer.validated_data, status=status.HTTP_200_OK
            )


class NewUserView(generics.ListCreateAPIView):
    """
    New User Create View
    """

    serializer_class = serializers.NewUserSerializer
    queryset = models.User.objects.all()

    def create(self, request, *args, **kwargs):
        user = request.data
        ser = self.serializer_class(data=user)
        ser.is_valid(raise_exception=True)
        new_user = ser.save()
        user_data = ser.data
        tokens = RefreshToken.for_user(new_user)
        refresh = str(tokens)
        access = str(tokens.access_token)

        return response.Response(
            {"user_data": user_data, "refresh_token": refresh, "access_token": access},
            status=status.HTTP_201_CREATED,
        )


class SearchView(generics.ListCreateAPIView):

    serializer_class = serializers.SearchSerializer
    queryset = models.SearchModel.objects.all()
    permission_classes = permissions.IsAuthenticated

    def get(self, request, *args, **kwargs):
        current_user = self.request.user
        start_datetime = self.request.query_params.get("start_datetime")
        end_datetime = self.request.query_params.get("end_datetime")
        if start_datetime and end_datetime:
            result = self.queryset.filter(
                timestamp__range=(start_datetime, end_datetime), user=current_user
            )
            contaxt = {
                "user_id": current_user.id,
                "payload": [
                    {"timestamp": i.timestamp, "input_values": i.input_values}
                    for i in result
                ],
            }
        else:
            result = self.queryset.filter(user=current_user)
            contaxt = {
                "user_id": current_user.id,
                "payload": [
                    {"timestamp": i.timestamp, "input_values": i.input_values}
                    for i in result
                ],
            }

        return response.Response(contaxt)

    def post(self, request, *args, **kwargs):
        current_user = self.request.user
        data = request.data
        input_values = data.get("input_values").split(",")
        search_value = data.get("search_value")
        data["user"] = current_user.id
        input_values = [int(x) for x in input_values]
        data["input_values"] = ",".join(
            str(i) for i in sorted((input_values), reverse=True)
        )

        ser = self.serializer_class(data=data)
        ser.is_valid(raise_exception=True)
        ser.save()

        if search_value in input_values:
            return response.Response("True")
        else:
            return response.Response("False")
