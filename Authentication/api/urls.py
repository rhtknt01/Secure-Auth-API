from django.urls import path
from api import views

#url examples 
"""
http://127.0.0.1:8000/api/countries/
http://127.0.0.1:8000/api/cities/?state_name=maharashtra
"""
urlpatterns = [
    path('countries/',views.CountryListView.as_view(),name='countries'),
    path('states/',views.StateListView.as_view(),name='states'),
    path('cities/',views.CityListView.as_view(),name='cities'),
    path('auth/register/',views.UserRegistrationView.as_view(),name='register'),
    path('auth/login/', views.UserLoginView.as_view(),name='login'),
    path('auth/profile/', views.UserProfileView.as_view(), name='profile'),
    path('auth/changepassword/', views.ChangeUserPasswordView.as_view(), name='change_password'),
    path('auth/token/refresh/', views.TokenRefreshView.as_view(), name='token_refresh')
]
