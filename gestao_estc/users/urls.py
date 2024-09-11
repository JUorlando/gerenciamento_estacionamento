from django.urls import path
from . import views

urlpatterns = [
    path("", views.UserView.as_view(), name="user-create"),
    path("<int:pk>/", views.UserDetailView.as_view(), name="user-detail"),
    path("login/", views.LoginView.as_view(), name="user-login"),
]
