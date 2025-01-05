from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.forms import UserChangeForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'gender', 'age', 'height', 'weight']




class CustomUserChangeForm(UserChangeForm):
    password = None
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'last_name', 'phone_number', 'gender', 'age', 'height', 'weight']
