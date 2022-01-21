from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
  username = models.CharField(max_length = 50, blank = True, null = True, unique = True)
  email = models.EmailField(max_length = 50, unique = True)
  full_name = models.CharField(max_length = 50, blank = True, null = True)
  phone_no = models.CharField(max_length = 10)

  bio = models.TextField(null=True,blank=True)
  avatar = models.ImageField(upload_to='avatars/',max_length=255, null=True, blank=True)
  
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username', 'first_name', 'last_name']
  def __str__(self):
      return "{}".format(self.email)