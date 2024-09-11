from django.urls import path
from . import views

urlpatterns = [
    path("users/", views.UserView.as_view(), name="user-create"),
    path("users/<int:pk>/", views.UserDetailView.as_view(), name="user-detail"),
    path("users/login/", views.LoginView.as_view(), name="user-login"),
]
