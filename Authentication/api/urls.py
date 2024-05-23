from django.urls import path, include
from api import views

urlpatterns = [
    path('auth/register/',views.UserRegistrationView.as_view()),
    path('auth/login/', views.UserLoginView.as_view())
]
