from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer, LoginSerializer
from .permissions import AccountOwner
from rest_framework import generics
from rest_framework.views import APIView, Request, Response, status
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken


class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [AccountOwner]

    queryset = User.objects.all()
    serializer_class = UserSerializer


class LoginView(APIView):
    queryset = User
    serializer_class = LoginSerializer

    def post(self, request: Request) -> Response:
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = authenticate(
            username=serializer.validated_data["username"],
            password=serializer.validated_data["password"],
        )

        if not user:
            return Response(
                {"detail": "No active account found with the given credentials"},
                status.HTTP_401_UNAUTHORIZED,
            )

        refresh = RefreshToken.for_user(user)

        token_dict = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }

        return Response(token_dict, status=status.HTTP_200_OK)
