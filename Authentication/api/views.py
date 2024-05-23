from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import permissions
from api.serializers import UserRegistrationSerializer, UserLoginSerializer, CityListSerializer, StateListSerializer, CountryListSerializer
from api.models import APIUser, City, State, Country
from rest_framework.response import Response
from rest_framework import status
from api.renderers import UserRenderer
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate

# Create your views here.
class UserRegistrationView(APIView):
    renderer_classes = [UserRenderer]
    # permission_classes = [permissions.Is]
    # authentication_classes = [authentication.TokenAuthentication]

    def post(self, request, format=None):
        # userdata = APIUser.objects.all()
        serializer = UserRegistrationSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'msg':'user Registration success!'}, status = status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)
    
class UserLoginView(APIView):
    renderer_classes = [UserRenderer]
    # permission_classes = [IsAuthenticated]

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data = request.data)

        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            if user is not None:
                return Response({'msg':'login success!'}, status=status.HTTP_200_OK)
            else:
                return Response({'msg':'invalid credentials'}, status=status.HTTP_404_NOT_FOUND)
            
class UserProfileView(APIView):
    renderer_classes = [UserRenderer]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        pass

class CountryListView(APIView):
    def get(self, request, format=None):
        country_list = []
        try:
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
                country = Country.objects.get(name=country_name)
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
                state = State.objects.get(name=state_name)
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