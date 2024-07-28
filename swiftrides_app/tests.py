from django.test import TestCase
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from .models import Car, Profile, Reservation

class PaymentTestCase(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a car
        self.car = Car.objects.create(name='Test Car', make='Test Make', model='Test Model', user=self.user, price='1000', is_available=True)

        # Create a reservation
        self.reservation = Reservation.objects.create(pickup='2024-04-12 12:00:00', dropoff='2024-04-15 12:00:00', pickup_location='Test Location', user=self.user, car=self.car)

    def test_payment_process(self):
        # Ensure the user is logged in (if needed)
        self.client.force_login(self.user)

        # Define the URL for initiating payment
        payment_url = reverse('initiatepayment')

        # Simulate a POST request to initiate payment
        response = self.client.post(payment_url, {'reservation_id': self.reservation.id})

        # Assert that the payment process redirects to the payment gateway (you may need to adjust this assertion based on your implementation)
        self.assertRedirects(response, 'makepayment')

        # Add more assertions as needed to verify the payment process