from rest_framework import serializers
from api.models import APIUser, Country, State, City

class UserRegistrationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type':'password'}, write_only=True)
    class Meta:
        model = APIUser
        fields = ['email', 'password', 'password2']
        extra_kwargs = {'password':{'write_only':True, 'style': {'input_type':'password'} }}

    def validate(self, data):
        password = data.get('password')
        password2 = data.get('password2')
        if password != password2:
            raise serializers.ValidationError('both passwords should be same')
        return data
    
    def create(self, validated_data):
        return APIUser.objects.create_user(**validated_data)
    
class UserLoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)
    # password = serializers.CharField()
    class Meta:
        model = APIUser
        fields = ['email', 'password']
        extra_kwargs = {'password':{'style':{'input_type':'password'}}}


class CountryListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Country
        fields = ['name']


class StateListSerializer(serializers.ModelSerializer):
    country = CountryListSerializer(read_only=True)

    class Meta:
        model = State
        fields = ['name', 'country']
        

class CityListSerializer(serializers.ModelSerializer):
    state = serializers.SerializerMethodField()
    class Meta:
        model = City
        fields = ['name', 'state']

    def get_state(self, obj):
        # Return only the name of the state
        return {'name': obj.state.name}


