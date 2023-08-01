from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.urls import reverse_lazy
from .forms import RegistrationForm, EditUserDataForm
from django.contrib.auth.views import PasswordChangeView

class UserCreate(generic.CreateView):
    form_class = RegistrationForm
    template_name = 'registration/create.html'
    success_url = reverse_lazy('login')

class UserUpdate(generic.UpdateView):
    form_class = EditUserDataForm
    template_name = 'registration/edit.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user

class PasswordsChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('password_success')

def password_success(self, request):
    return render(request, 'registration/password_success.html')
