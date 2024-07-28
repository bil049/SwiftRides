from django import forms
from django.forms import ModelForm 
from .models import *
from django.forms.widgets import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AccountForm(ModelForm):
    def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super(AccountForm, self).__init__(*args, **kwargs)
            if user:
                self.fields['user'].initial = user  
                self.fields['user'].widget = TextInput(attrs={'readonly': 'readonly'})
    class Meta:
        model = Account
        fields = ['dateofbirth', 'user', 'fullname', 'phonenumber']
        widgets = {
            'dateofbirth': forms.DateInput(attrs={'type': 'date'}),
        }

class ReservationForm(ModelForm):
     def __init__(self, *args, **kwargs):
        car_id = kwargs.pop('car_id', None)
        super(ReservationForm, self).__init__(*args, **kwargs)
        if car_id:
            self.fields['car'].initial = car_id

     def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super(ReservationForm, self).__init__(*args, **kwargs)
            if user:
                self.fields['user'].initial = user  
                self.fields['user'].widget = TextInput(attrs={'readonly': 'readonly'})
                self.fields['pickup'].widget = DateTimeInput(attrs={'type': 'datetime-local'})
                self.fields['dropoff'].widget = DateTimeInput(attrs={'type': 'datetime-local'})

     class Meta:
          model = Reservation
          fields = ['user', 'pickup', 'dropoff', 'pickup_location']

class PaymentForm(ModelForm):

    email = forms.EmailField(widget=forms.EmailInput(attrs={'readonly': 'readonly'}))
    amount = forms.IntegerField(widget=forms.NumberInput(attrs={'readonly': 'readonly'}))
    
    class Meta:
          model = Payment
          fields = ['email', 'amount']
