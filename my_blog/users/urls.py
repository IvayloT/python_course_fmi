from django.urls import path
from .views import UserCreate, UserUpdate, PasswordsChangeView
from django.contrib.auth import views as auth_views
from . import views


urlpatterns = [
    path('registration/', UserCreate.as_view(), name='registration'),
    path('edit/', UserUpdate.as_view(), name='edit_user'),
    path('password/', PasswordsChangeView.as_view(template_name='registration/change-password.html')),
    path('password_success/', views.password_success, name='password_success'),

]
