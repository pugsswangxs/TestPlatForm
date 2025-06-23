from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .serializers import CustomTokenObtainPairSerializer, CustomTokeRefreshSerializer, UserRegisterSerializer
from rest_framework.generics import CreateAPIView


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


login_view_pair = CustomTokenObtainPairView.as_view()


class RefreshTokenView(TokenRefreshView):
    serializer_class = CustomTokeRefreshSerializer


login_refresh_view = RefreshTokenView.as_view()

class RegisterView(CreateAPIView):
    serializer_class = UserRegisterSerializer

register_view = RegisterView.as_view()