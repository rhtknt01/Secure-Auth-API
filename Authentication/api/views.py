#rest framework imports 
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken as JWTRefreshToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError, AuthenticationFailed
from rest_framework.views import APIView

#django imports
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.contrib.auth import authenticate
from django.apps import apps

#custom imports
from api.serializers import UserRegistrationSerializer, UserLoginSerializer, CityListSerializer, StateListSerializer, CountryListSerializer, ChangeUserPasswordSerializer
from api.renderers import UserRenderer
from api.customClasses import CustomIsAuthenticated
from api.utilities import get_tokens_for_user, set_refresh_token_cookie, set_access_token_cookie, blacklist_token
from api.constants import *



# Create your views here.
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    # permission_classes = [permissions.Is]
    # authentication_classes = [authentication.TokenAuthentication]

    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response({'code':REGISTRATION_SUCCESS,'msg':SUCCESS_MESSAGES[REGISTRATION_SUCCESS]}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, format=None):
        serializer = UserLoginSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            tokens = None
            refresh_token = None
            access_token = None

            #setting tokens for user(user_id field)
            if user is not None:
                # Check if there is a valid refresh token for the user
                RefreshToken = apps.get_model('api', 'RefreshToken')
                db_refresh_token = RefreshToken.objects.filter(user=user, revoked=False, expired_at__gt=timezone.now()).first()

                tokens = get_tokens_for_user(user)
                access_token = tokens.get('access')
                
                if db_refresh_token:
                    refresh_token = db_refresh_token.token
                else:
                    refresh_token = tokens.get('refresh')
                    RefreshToken.objects.create(user=user, token=refresh_token, expired_at=timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'])
                
            if user is not None:
                response = Response({'code':LOGIN_SUCCESS,'msg': SUCCESS_MESSAGES[LOGIN_SUCCESS]}, status=status.HTTP_200_OK)
                set_refresh_token_cookie(response, refresh_token)
                set_access_token_cookie(response, access_token)

                return response
            else:
                return Response({'code':INVALID_CREDENTIALS,'msg':ERROR_MESSAGES[INVALID_CREDENTIALS]}, status=status.HTTP_404_NOT_FOUND)


class TokenRefreshView(APIView):
    def get(self, request, format=None):
        refresh_token = request.COOKIES.get('refresh_token')
        access_token = request.COOKIES.get('access_token')
        if not refresh_token:
            raise AuthenticationFailed({'code':REFRESH_TOKEN_NOT_FOUND,'msg':ERROR_MESSAGES[REFRESH_TOKEN_NOT_FOUND]})
        
        try:
            #blacklist old access token
            blacklist_token(access_token)

            # Use the provided refresh token to generate a new access token
            jwt_refresh_token = JWTRefreshToken(refresh_token)
            new_access_token = str(jwt_refresh_token.access_token)

            response = Response({'code':TOKEN_REFRESH_SUCCESS,'msg':SUCCESS_MESSAGES[TOKEN_REFRESH_SUCCESS]}, status=status.HTTP_200_OK)
            set_access_token_cookie(response, new_access_token)
            return response
        
        except (TokenError, InvalidToken):
            # Optionally, blacklist the old refresh token if it has expired
            RefreshToken = apps.get_model('api','RefreshToken')
            db_refresh_token = RefreshToken.objects.filter(token=refresh_token).first()
            if db_refresh_token and not db_refresh_token.is_valid():
                db_refresh_token.revoked = True
                db_refresh_token.save()

                #refresh token expired login again
                login_url = reverse('login')
                return Response({'code':REFRESH_TOKEN_EXPIRED,'msg':ERROR_MESSAGES[REFRESH_TOKEN_EXPIRED], 'login_url': login_url}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [CustomIsAuthenticated]

    def get(self, request, format=None):
        return Response({'code':LOGIN_SUCCESS,'msg': SUCCESS_MESSAGES[LOGIN_SUCCESS]}, status=status.HTTP_200_OK)


class ChangeUserPasswordView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [CustomIsAuthenticated]

    def post(self, request, format=None):
        user = request.user
        serializer = ChangeUserPasswordSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user.set_password(serializer.validated_data['password2'])
            user.save()

            # Blacklist the current access token
            access_token = request.COOKIES.get('access_token')
            blacklist_token(access_token)

            #Blacklist the current refresh token 
            refresh_token = request.COOKIES.get('refresh_token')
            RefreshToken = apps.get_model('api','RefreshToken')
            refresh_token_obj = RefreshToken.objects.filter(token=refresh_token).first()

            if refresh_token_obj:
                refresh_token_obj.revoked = True
                refresh_token_obj.save()

            login_url = reverse('login')
            response = Response({'code':PASSWORD_CHANGED_SUCCESS,'msg': SUCCESS_MESSAGES[PASSWORD_CHANGED_SUCCESS], 'redirect': login_url}, status=status.HTTP_200_OK)

            return response

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlackListTokenView(APIView):
    renderer_classes = [UserRenderer]
    def get(self, request, format=None):
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            raise AuthenticationFailed({'msg':ERROR_MESSAGES[ACCESS_TOKEN_NOT_FOUND]})
    



















class CountryListView(APIView):
    def get(self, request, format=None):
        country_list = []
        try:
            Country = apps.get_model('api','Country')
            all_countries = Country.objects.all()
            serializer = CountryListSerializer(all_countries, many=True)
            for dataItem in serializer.data:
                country_name = dataItem.get('name',None)
                country_list.append(country_name)

            return Response(country_list)
        
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class StateListView(APIView):
    def get(self, request, format=None):
        country_name = request.query_params.get('country_name', None)
        print(country_name)
        if country_name:
            try:
                Country = apps.get_model('api','Country')
                country = Country.objects.get(name=country_name)
                State = apps.get_model('api','State')
                states = State.objects.filter(country=country)
            except Country.DoesNotExist:
                return Response({'error': 'Country not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            states = State.objects.all()
        
        serializer = StateListSerializer(states, many=True)
        state_list = []
        for dataItem in serializer.data:
            state_name = dataItem.get('name',None)
            state_list.append(state_name)
            
        return Response(state_list, status=status.HTTP_200_OK)
    
class CityListView(APIView):
    def get(self, request, format=None):
        state_name = request.query_params.get('state_name', None)
        if state_name:
            try:
                State = apps.get_model('api','State')
                state = State.objects.get(name=state_name)
                City = apps.get_model('api','City')
                cities = City.objects.filter(state=state)
            except State.DoesNotExist:
                return Response({'error': 'State not found'}, status=status.HTTP_404_NOT_FOUND)
        else:
            cities = City.objects.all()
        
        serializer = CityListSerializer(cities, many=True)
        city_list = []
        for dataItem in serializer.data:
            city_name = dataItem.get('name',None)
            city_list.append(city_name)

        return Response(city_list, status=status.HTTP_200_OK)
    

    """
    eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE2Njg5NzA1LCJpYXQiOjE3MTY2ODg1MDUsImp0aSI6ImM4YTU1NTM1NzZjYjRhOTlhYTM2MjRkOWYzZDA1ZDNiIiwidXNlcl9pZCI6IjFlNDBmZjg4NGYwYiJ9.52t_pKoRYT08CQ-huc5vNKPQ3sZyqupscDSAAGbyU5c
    """