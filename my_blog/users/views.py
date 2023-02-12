from django.shortcuts import render
from django.views import generic
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

class UserCreate(generic.CreateView):
    form_class = UserCreationForm
    template_name = 'registration/create.html'
    success_url = reverse_lazy('login')

class UserUpdate(generic.UpdateView):
    form_class = UserCreationForm
    template_name = 'registration/edit.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.request.user
