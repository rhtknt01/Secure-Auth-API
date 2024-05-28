import hashlib, time
from rest_framework_simplejwt.tokens import RefreshToken
from django.apps import apps


#custom functions 

def is_token_blacklisted(token):
    BlackListedToken = apps.get_model('api','BlackListedToken')
    return BlackListedToken.objects.filter(token=token).exists()


def blacklist_token(token):
    if not is_token_blacklisted(token):
        BlackListedToken = apps.get_model('api','BlackListedToken')
        BlackListedToken.objects.create(token=token)

def generate_unique_user_id(user):
    role_prefix = '1'  # Default to regular user
    if user.is_admin:
        role_prefix = '3'
    elif user.is_staff:
        role_prefix = '2'

    # Using email and current time to generate a unique identifier
    unique_string = f"{user.email}{int(time.time())}"
    unique_hash = hashlib.sha256(unique_string.encode()).hexdigest()[:11]
    return f"{role_prefix}{unique_hash}"


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }

def set_refresh_token_cookie(response, refresh_token):
    response.set_cookie(
        key='refresh_token',
        value=refresh_token,
        httponly=True,  # HttpOnly flag to prevent JavaScript access
        secure=False,    # Secure flag to ensure it's only sent over HTTPS
        samesite='Lax',  # SameSite attribute
        max_age=60*60*24*30  # Set max age to 30 days (or as required)
    )

def set_access_token_cookie(response, access_token):
    response.set_cookie(
        key='access_token',
        value=access_token,
        httponly=True,
        secure=False,
        samesite='Lax',
        max_age=60*15  # 15 minutes
    )












# from django.conf import settings
# import jwt
# from django.utils import timezone
# from datetime import timedelta
# import uuid

# def generate_refresh_token(user):
#     jti = str(uuid.uuid4())
#     user_id_field = settings.SIMPLE_JWT['USER_ID_FIELD']
#     user_id_claim = settings.SIMPLE_JWT['USER_ID_CLAIM']
#     user_id_value = getattr(user, user_id_field)

#     refresh_token = jwt.encode({
#         'token_type': 'refresh',
#         'exp': (timezone.now() + settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME']).timestamp(),
#         'iat': timezone.now().timestamp(),
#         'jti': jti,
#         user_id_claim: user_id_value  # Dynamic key
#     }, settings.SIMPLE_JWT['SIGNING_KEY'], algorithm=settings.SIMPLE_JWT['ALGORITHM'])
    
#     return refresh_token

# def generate_access_token(user):
#     user_id_field = settings.SIMPLE_JWT['USER_ID_FIELD']
#     user_id_claim = settings.SIMPLE_JWT['USER_ID_CLAIM']
#     user_id_value = getattr(user, user_id_field)

#     access_token = jwt.encode({
#         'token_type': 'access',
#         'exp': (timezone.now() + settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME']).timestamp(),
#         'iat': timezone.now().timestamp(),
#         'jti': str(uuid.uuid4()),
#         user_id_claim: user_id_value  # Dynamic key
#     }, settings.SIMPLE_JWT['SIGNING_KEY'], algorithm=settings.SIMPLE_JWT['ALGORITHM'])
    
#     return access_token


# # utils.py

# from datetime import timedelta
# from django.utils import timezone
# import uuid
# from .models import RefreshToken

# def generate_refresh_token(user):
#     expiration_time = timezone.now() + timedelta(days=30)
#     refresh_token = RefreshToken.objects.create(
#         user=user,
#         expired_at=expiration_time
#     )
#     return str(refresh_token.token)

# def generate_access_token(user):
#     expiration_time = timezone.now() + timedelta(minutes=15)
#     payload = {
#         'user_id': user.id,
#         'exp': expiration_time,
#         'iat': timezone.now(),
#         'jti': str(uuid.uuid4())
#     }
#     token = jwt.encode(payload, 'your_secret_key', algorithm='HS256')
#     return token



# from rest_framework_simplejwt.tokens import AccessToken

# def get_user_from_token(token):
#     try:
#         # Decode the token
#         access_token = AccessToken(token)
#         # Get the user ID from the token
#         user_id = access_token.get('user_id')
#         # Retrieve the user from the database
#         user = APIUser.objects.get(email=user_id)
#         return user
#     except Exception as e:
#         return None
