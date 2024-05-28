from rest_framework.permissions import BasePermission
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework.exceptions import AuthenticationFailed
import datetime
from django.urls import reverse
from django.apps import apps
from api.utilities import is_token_blacklisted
from api.constants import *

class CustomIsAuthenticated(BasePermission):
    def has_permission(self, request, view):
        # Check if the access token is available
        access_token = request.COOKIES.get('access_token')
        if not access_token:
            raise AuthenticationFailed({'code': ACCESS_TOKEN_NOT_FOUND,'msg': ERROR_MESSAGES[ACCESS_TOKEN_NOT_FOUND]})
        
        if is_token_blacklisted(access_token):
            raise AuthenticationFailed({'code':ACCESS_TOKEN_BLACKLISTED,'msg':ERROR_MESSAGES[ACCESS_TOKEN_BLACKLISTED]})

        try:
            # Decode the access token
            decoded_token = AccessToken(access_token)
            
            # Check if the access token is expired
            expiration_timestamp = decoded_token['exp']
            expiration_time = datetime.datetime.fromtimestamp(expiration_timestamp, datetime.timezone.utc)
            current_time = datetime.datetime.now(datetime.timezone.utc)
            if expiration_time < current_time:
                raise AuthenticationFailed({'code':ACCESS_TOKEN_EXPIRED, 'msg':ERROR_MESSAGES[ACCESS_TOKEN_EXPIRED]})

            # Get user ID from the token and set it to request.user
            user_id = decoded_token['user_id']
            try:
                APIUser = apps.get_model('api', 'APIUser')
                user = APIUser.objects.get(user_id=user_id)
                request.user = user
            except APIUser.DoesNotExist:
                raise AuthenticationFailed({'code':USER_NOT_EXISTS, 'msg':ERROR_MESSAGES[USER_NOT_EXISTS]})

        except (TokenError, InvalidToken):
            # If the access token is invalid or expired, provide redirect info for refresh
            refresh_token = request.COOKIES.get('refresh_token')
            if not refresh_token:
                raise AuthenticationFailed({'code':REFRESH_TOKEN_NOT_FOUND, 'msg':ERROR_MESSAGES[REFRESH_TOKEN_NOT_FOUND]})

            # Construct the redirect URL for token refresh
            refresh_url = reverse('token_refresh')
            raise AuthenticationFailed({
                'redirect_url': refresh_url,
                'code':ACCESS_TOKEN_EXPIRED,
                'msg': ERROR_MESSAGES[ACCESS_TOKEN_EXPIRED]
            })

        return True
