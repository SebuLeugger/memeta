from django.urls import path
from .views import UserRegisterView, NotImplementedView


urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('password/', NotImplementedView, name='not_implemented'),
]
