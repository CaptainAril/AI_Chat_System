import uuid

from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager,
                                        PermissionsMixin)
from django.db import models


# User Manager
class CustomUserManager(BaseUserManager):
    def create_user(self, username, password):
        user = self.model(username=username)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(username=username, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self.db)
        return user

# User model
class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(primary_key=True, max_length=50, unique=True, null=False)
    password = models.CharField(max_length=128, null=False)
    tokens = models.IntegerField(default=4000)
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    
    objects = CustomUserManager()
    
    def __str__(self):
        return self.username
    
    
# Chat model
class Chat(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    response = models.TextField(null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    
