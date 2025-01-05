from django.shortcuts import render
from accounts.forms import CustomUserCreationForm, CustomUserChangeForm
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import views as auth_views

class CustomUserCreationForm(CreateView):
    form_class = CustomUserCreationForm
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')


class ProfileView(LoginRequiredMixin, UpdateView):
    form_class = CustomUserChangeForm
    template_name = 'registration/profile.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self):
        return self.request.user


class PasswordChangeView(LoginRequiredMixin, auth_views.PasswordChangeView):
    template_name = 'registration/password_change.html'
    success_url = reverse_lazy('profile')


