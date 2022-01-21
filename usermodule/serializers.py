from django.contrib.auth import models
from rest_framework import serializers, status
from rest_framework import fields
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from django.contrib.auth.password_validation import validate_password

from usermodule.models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def get_token(cls, user):
#         token = super(MyTokenObtainPairSerializer, cls).get_token(user)
#         # Add custom claims
#         token['username'] = user.username
#         return token

class RegisterSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            required=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    phone_no = serializers.CharField( max_length=10,min_length=10,trim_whitespace=True,
            validators=[UniqueValidator(queryset=User.objects.all())]
            )
    full_name = serializers.CharField( required=True )
    username = serializers.CharField( required=True )
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    
    class Meta:
        model = User
        fields = ('id', 'email', 'username','full_name','phone_no','password',)
      
    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            full_name=validated_data['full_name'],
            phone_no=validated_data['phone_no']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(write_only=True, required=True)
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    confirm_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('old_password', 'password', 'confirm_password')

    def validate(self, attrs):
        if attrs['password'] != attrs['confirm_password']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError({"old_password": "Old password is not correct"})
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance

class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
            validators=[UniqueValidator(queryset=User.objects.all(),message="This email already exist.")]
            )
    phone_no = serializers.CharField( max_length=10,min_length=10,trim_whitespace=True,
            validators=[UniqueValidator(queryset=User.objects.all(),message="This phone number already exist.")]
            )
    username = serializers.CharField( max_length=50,
            validators=[UniqueValidator(queryset=User.objects.all(),message="This username already exist.")]
            )
    full_name = serializers.CharField(max_length=50),
    bio = serializers.CharField(style={'base_template': 'textarea.html'})

    class Meta:
        model = User
        fields = ('full_name', 'username', 'bio', 'email','phone_no')

class UploadImageSerializer(serializers.ModelSerializer):
    avatar = serializers.ImageField()

    class Meta:
        model = User
        fields = ['avatar']


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs['refresh']
        return attrs

    def save(self,**kwargs):
        try:
            token = RefreshToken(self.token)
            print("token is",token)
            token.blacklist()
        except TokenError:
            return Response(status=status.HTTP_400_BAD_REQUEST)