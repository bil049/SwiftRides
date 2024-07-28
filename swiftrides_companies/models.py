from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser

class Car(models.Model):
    image = models.ImageField(null=True, upload_to="images/")
    name = models.CharField(max_length=100)
    make = models.CharField(max_length=100)
    model = models.CharField(max_length = 100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    price = models.CharField(max_length=100, null=True)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.name} - {self.model}"
    

    @property
    def company_name(self):
        if self.user.profile:
            return self.user.profile.company_name
        return None


class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)    
    company_name = models.CharField(verbose_name='Company Name', max_length = 100, null=True)
    location = models.CharField(max_length=100)

    def __str__(self):
        return self.company_name




