from django.db import models
from django.contrib.auth.models import User
from swiftrides_companies.models import *
from django.utils import timezone
import uuid, secrets
from .paystack import PayStack


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    reference = models.CharField(max_length=255, unique=True)
    email = models.CharField(max_length=100, null=True)
    amount = models.PositiveIntegerField()
    verified = models.BooleanField(default=True)
    reservation = models.ForeignKey('Reservation', on_delete=models.SET_NULL, null=True)
    paystack_reference = models.CharField(max_length=255, null=True)  # Add this field
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.reference
    
    def save(self, *args, **kwargs):
        while not self.reference:
            reference = secrets.token_urlsafe(50)
            object_with_similar_reference = Payment.objects.filter(reference=reference)
            if not object_with_similar_reference:
                self.reference = reference
        super().save(*args, **kwargs)

    def amount_value(self) -> int:
        return self.amount*100     

    def verify_payment(self):
        paystack = PayStack()  
        status, result = paystack.verify_payment(self.reference, self.amount_value())
        if status:
            if result['amount'] == self.amount_value():
                self.verified = True 
            self.save()
        if self.verified:
            return True
        return False       

class Reservation(models.Model):
    pickup = models.DateTimeField(verbose_name='Pickup Date')
    dropoff = models.DateTimeField(verbose_name='Dropoff Date')
    pickup_location = models.CharField(verbose_name='Pickup Location', max_length=100)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    car = models.ForeignKey(Car, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=20, default='pending')


    def __str__(self):
        return f"{self.user.username} - {self.car.name}"

    def save(self, *args, **kwargs):
        if not self.pk:  
            self.car.is_available = False  
            self.car.save()  # Save the car
        super().save(*args, **kwargs) 

    def delete(self, *args, **kwargs):
        self.car.is_available = True  # Mark the car as available
        self.car.save()  # Save the car
        super().delete(*args, **kwargs)  # Call the original delete method

    def check_and_update_car_availability(self):
        if self.dropoff < timezone.now():  # If dropoff date has passed
            self.car.is_available = True  # Mark the car as available
            self.car.save()  # Save the car


class Account(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)  
    fullname = models.CharField(max_length=100, verbose_name='Full Name', null=True)  
    dateofbirth = models.DateField(verbose_name='Date Of Birth', null=True)
    phonenumber = models.CharField(verbose_name='Phone Number', max_length = 100, null=True)

    def __str__(self):
        return self.fullname
    # location = models.CharField(max_length=100)