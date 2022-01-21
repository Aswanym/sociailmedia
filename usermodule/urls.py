from django.urls import path
from usermodule.views import  RegisterView, ChangePasswordView, UpdateProfileView, UploadImageViewSet, LogoutView
from rest_framework_simplejwt.views import TokenRefreshView, TokenObtainPairView


urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('change_password/<int:pk>/', ChangePasswordView.as_view(), name='auth_change_password'),
    path('update_profile/<int:pk>/', UpdateProfileView.as_view(), name='auth_update_profile'), 
    path('upload_picture/<int:pk>/', UploadImageViewSet.as_view({'get':'retrieve','put':'update','patch':'partial_update','delete':'destroy'}), name='auth_upload_picture'),  
]
