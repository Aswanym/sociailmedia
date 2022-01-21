from rest_framework import mixins, serializers, viewsets
from .serializers import (RegisterSerializer, ChangePasswordSerializer, 
                            UpdateUserSerializer, UserSerializer, UploadImageSerializer,LogoutSerializer)
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser,FormParser
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework import status

from rest_framework import generics
from django.contrib.auth import get_user_model

User = get_user_model()

#to list all the users.
class UserListViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

#login
# class MyObtainTokenPairView(TokenObtainPairView):
#     permission_classes = (AllowAny,)
#     serializer_class = MyTokenObtainPairSerializer

#register
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

#change password
class ChangePasswordView(generics.UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = ChangePasswordSerializer

#update profile
class UpdateProfileView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    serializer_class = UpdateUserSerializer


#retrieve, update, delete profile picture
class UploadImageViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    parser_classes = [ MultiPartParser,FormParser]
    serializer_class = UploadImageSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({"message":"Image deleted successfully"},status=status.HTTP_204_NO_CONTENT)

#logout
class LogoutView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"successfully logged out."},status=status.HTTP_204_NO_CONTENT)

        