from django import forms
from django.forms import ModelForm 
from django.forms.widgets import *
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CarForm(ModelForm):
    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        # self.fields['image'].required = False
        super(CarForm, self).__init__(*args, **kwargs)
        if user:
            self.fields['user'].initial = user  
            self.fields['user'].widget = TextInput(attrs={'readonly': 'readonly'})
    image = forms.ImageField(required=False)
    class Meta:
        model = Car
        fields = ['user','image', 'name', 'make', 'model', 'price']
 
class ProfileForm(ModelForm):
    def __init__(self, *args, **kwargs):
            user = kwargs.pop('user', None)
            super(ProfileForm, self).__init__(*args, **kwargs)
            if user:
                self.fields['user'].initial = user  
                self.fields['user'].widget = TextInput(attrs={'readonly': 'readonly'})
    class Meta:
        model = Profile
        fields = ['company_name', 'user', 'location']



class CreateUserForm(UserCreationForm):
    # logo = forms.ImageField()
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


