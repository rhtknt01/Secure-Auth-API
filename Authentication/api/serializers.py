from rest_framework import serializers
from django.apps import apps
from api.constants import *

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)

    class Meta:
        model = apps.get_model('api', 'APIUser')
        fields = ['email', 'password', 'password2']
        extra_kwargs = {'password':{'write_only':True, 'style': {'input_type':'password'} }}

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError({'code':DISSIMILAR_PASSWORD,'msg':ERROR_MESSAGES[DISSIMILAR_PASSWORD]})
        return data
    
    def create(self, validated_data):
        APIUser = apps.get_model('api', 'APIUser')
        return APIUser.objects.create_user(**validated_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        model = apps.get_model('api', 'APIUser')
        fields = ['email', 'password']
        extra_kwargs = {'password':{'style':{'input_type':'password'}}}


# class TokenRefreshSerializer(serializers.Serializer):
#     refresh = serializers.CharField()

class ChangeUserPasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)
    password2 = serializers.CharField(max_length=255, style={'input_type':'password'}, write_only=True)

    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        if password != password2:
            raise serializers.ValidationError({'code':DISSIMILAR_PASSWORD,'msg':ERROR_MESSAGES[DISSIMILAR_PASSWORD]})
        return attrs

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('api', 'APIUserProfile')
        fields = '__all__'

class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = apps.get_model('api', 'Country')
        fields = ['name']


class StateListSerializer(serializers.ModelSerializer):
    country = CountryListSerializer(read_only=True)

    class Meta:
        model = apps.get_model('api', 'State')
        fields = ['name', 'country']
        

class CityListSerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField()
    class Meta:
        model = apps.get_model('api', 'City')
        fields = ['name', 'state']

    def get_state(self, obj):
        # Return only the name of the state
        return {'name': obj.state.name}


