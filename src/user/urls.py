from django.urls import path

# from rest_framework_simplejwt.views import (
#     TokenObtainPairView,
#     TokenRefreshView,
#     TokenVerifyView,
# )

from user import views

urlpatterns = [
    path("token/", views.MyTokenObtainPairView.as_view()),
    path("create_user/", views.NewUserView.as_view()),
    path("search/", views.SearchView.as_view()),
]
