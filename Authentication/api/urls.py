from django.urls import path, include
from api import views

#url examples 
"""
http://127.0.0.1:8000/api/countries/
http://127.0.0.1:8000/api/cities/?state_name=maharashtra
"""
urlpatterns = [
    path('auth/register/',views.UserRegistrationView.as_view(),name='register'),
    path('auth/login/', views.UserLoginView.as_view(),name='login'),
    path('countries/',views.CountryListView.as_view(),name='countries'),
    path('states/',views.StateListView.as_view(),name='states'),
    path('cities/',views.CityListView.as_view(),name='cities'),
]
