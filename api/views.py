from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework import authentication

from .serializers import *
import jwt, datetime

# Create your views here.

#Class to check whether the user is authenticated or not
class UserAuthenticated(authentication.BaseAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('jwt') #Obtain the JWT from cookies

        if not token:
            raise AuthenticationFailed('Unauthorized') #Throw auth error if no cookies are present
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256']) #decode the token
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthorized') #throw an error if the token is expired
        user = User.objects.get(id = payload['id']) 
        return (user, None)

#A base view to add authentication to relevant views
class BaseView(APIView):
    authentication_classes = [UserAuthenticated]

#Registration view
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True) #Check if the given data is valid
        serializer.save()
        response = Response()
        response.data={
            'msg': "User successfully registered."
        }
        #return Response(serializer.data)
        return response

#Login view
class LoginView(APIView):
    def post(self, request):
        username = request.data['username']
        password = request.data['password']

        user = User.objects.filter(username=username).first() #Since only a single user exists with any username, filter the first result

        if user is None: #Check if there exists a user with given username
            raise AuthenticationFailed('User does not exist.')
        
        if not user.check_password(password): #Check if the password given is correct
            raise AuthenticationFailed('Incorrect password.')
        
        #Creating the payload required to generate the token
        payload = {
            'id': user.id, #the user id associated with the token
            'exp': datetime.datetime.utcnow() + datetime.timedelta(days=7), #exp displays the expiration time of the token
            'iat': datetime.datetime.utcnow() #iat displays when the jwt was created
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256') #encoding the token using a hashing algorithm

        response = Response() #Create a response object so that the token can be set as a cookie

        response.set_cookie(key='jwt', value=token, httponly=True) 
        response.data={
            'jwt': token
        }

        return response
    
#Logout view
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        token = request.COOKIES.get('jwt') #Obtain the JWT from cookies

        if not token:
            raise AuthenticationFailed('No account is logged in.') #Throw auth error if no cookies are present
        
        response.delete_cookie('jwt') #Delete the cookie during logout
        response.data = {
            'message': 'Logout successful.'
        }
        return response

#A view to update data related to aircrafts or delete one
class UpdateAircraftView(generics.RetrieveUpdateDestroyAPIView, BaseView):
    serializer_class = AircraftSerializer
    queryset = Aircraft.objects.all()

#A view to get aircrafts and to create one
class AircraftView(generics.ListCreateAPIView, BaseView):
    serializer_class = AircraftSerializer
    queryset = Aircraft.objects.all()

#A view to update data related to airlines or delete an airline
class UpdateAirlineView(generics.RetrieveUpdateDestroyAPIView, BaseView):
    serializer_class = AirlineSerializer
    queryset = Airline.objects.all()

#A view to get airlines and to create one
class AirlineView(generics.ListCreateAPIView, BaseView):
    serializer_class = AirlineSerializer
    queryset = Airline.objects.all()