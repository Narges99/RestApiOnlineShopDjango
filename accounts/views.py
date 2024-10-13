from drf_yasg.utils import swagger_auto_schema
from rest_framework.generics import RetrieveUpdateAPIView, ListAPIView, CreateAPIView, DestroyAPIView
from django.contrib.auth.models import User
from rest_framework_simplejwt.views import TokenObtainPairView, TokenBlacklistView
from .serializers import UserSerializer, UserUpdateSerializer
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny



class UserRetrieveUpdateView(RetrieveUpdateAPIView):

    queryset = User.objects.all()
    serializer_class = UserUpdateSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class UserListView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

class UserCreateView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]


class UserDeleteView(DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class LoginUser(TokenObtainPairView):
    pass


class LogoutUser(TokenBlacklistView):
    pass
