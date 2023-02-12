from django.urls import path
from .views import UserCreate, UserUpdate


urlpatterns = [
    path('registration/', UserCreate.as_view(), name='registration'),
    path('edit/', UserUpdate.as_view(), name='edit_profile')
]
