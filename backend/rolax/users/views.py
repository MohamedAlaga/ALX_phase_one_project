from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer , ItemsSerializer
from .models import User
import jwt , datetime
# Create your views here.

class Register(APIView):
  def post(self, request):
    serizlizer = UserSerializer(data=request.data)
    serizlizer.is_valid(raise_exception=True)
    serizlizer.save()
    return Response(serizlizer.data)
  
class Login(APIView):
  def post(self, request):
    email = request.data['email']
    password = request.data['password']
    user = User.objects.filter(email=email).first()

    if user is None:
      raise AuthenticationFailed('User not found!')
    
    if not user.check_password(password):
      raise AuthenticationFailed('Incorrect password!')
    
    payload = {
      'id': user.id,
      'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
      'iat': datetime.datetime.utcnow()
    }

    token = jwt.encode(payload, 'secret', algorithm='HS256')
    response = Response()
    response.set_cookie(key='token', value=token, httponly=True)
    response.set_cookie(key='pharma_id', value=user.manager.id, httponly=True)
    response.data = {'token': token , 'pharma_id': user.manager.id}

    return response
  
class UserView(APIView):
  def get(self, request):
    token = request.COOKIES.get('token')

    if not token:
      raise AuthenticationFailed('Unauthenticated!')
    
    try:
      payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed('Unauthenticated!')
    
    user = User.objects.filter(id=payload['id']).first()
    serizlizer = UserSerializer(user)
    return Response(serizlizer.data)

class Logout(APIView):
  def post(self, request):
    response = Response()
    response.delete_cookie('token')
    response.delete_cookie('pharma_id')
    response.data = {'message': 'success'}
    return response

class ItemsView(APIView):
   def post(self, request):
    owner = request.COOKIES.get('pharma_id')
    data = request.data.copy()
    data['owner'] = owner
    serizlizer = ItemsSerializer(data=data)
    serizlizer.is_valid(raise_exception=True)
    serizlizer.save()
    
    return Response(serizlizer.data)