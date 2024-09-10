from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from .serializers import UserSerializer , ItemsSerializer , PurchaseReceiptSerializer
from .models import User , Items
from rest_framework import status
from .models import purchaseReciept
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

class addItemsView(APIView):
   def post(self, request):
    owner = request.COOKIES.get('pharma_id')
    data = request.data.copy()
    data['owner'] = owner
    serizlizer = ItemsSerializer(data=data)
    serizlizer.is_valid(raise_exception=True)
    serizlizer.save()
    
    return Response(serizlizer.data)

class purchaseReceiptBulkCreateView(APIView):
  def post(self, request):
    owner = request.COOKIES.get('pharma_id')
    data = request.data.copy()
    last_receipt = purchaseReciept.objects.last()
    recieptNumber = last_receipt.recieptNumber + 1 if last_receipt else 1
    for item_data in data:
      try:
        item = Items.objects.get(id=item_data['id'])
      except Items.DoesNotExist:
        return Response({"error": f"Item with id {item_data['id']} does not exist"}, status=status.HTTP_400_BAD_REQUEST)
      serializer_data = {
                'item': item.id,
                'quantity': item_data['quantitiy'],
                'price': item_data['price'],
                'owner': owner,
                'recieptNumber': recieptNumber
            }
      serializer = PurchaseReceiptSerializer(data=serializer_data, context={'request': request})
      if serializer.is_valid():
        serializer.save()
      else:
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response({"message": "Purchase receipts created successfully"}, status=status.HTTP_201_CREATED)

class getCurentUserlastPurchaseReciept(APIView):
  def get(self, request):
    owner = request.COOKIES.get('pharma_id')
    if owner is None:
      return Response({"message": "No user found"}, status=status.HTTP_403_FORBIDDEN)
    last_receipt = purchaseReciept.objects.filter(owner=owner).last()
    if last_receipt :
      reciepts = purchaseReciept.objects.filter(recieptNumber=last_receipt.recieptNumber , owner=owner)
      data = []
      for reciept in reciepts:
        data.append({
          'item_id': reciept.item.id,
          'item_name': reciept.item.name,
          'quantity': reciept.quantity,
          'price': reciept.price,
          'owner': reciept.owner.id,
          'recieptNumber': reciept.recieptNumber
        })
      return Response(data)
    return Response({"message": "No purchase receipt found"}, status=status.HTTP_404_NOT_FOUND)

class getUserPurchaserecieptsByNumber(APIView):
  def get(self, request, id):
    owner = request.COOKIES.get('pharma_id')
    if owner is None:
      return Response({"message": "No user found"}, status=status.HTTP_403_FORBIDDEN)
    reciepts = purchaseReciept.objects.filter(recieptNumber=id , owner=owner)
    data = []
    if reciepts :
      for reciept in reciepts:
        data.append({
          'item_id': reciept.item.id,
          'item_name': reciept.item.name,
          'quantity': reciept.quantity,
          'price': reciept.price,
          'owner': reciept.owner.id,
          'recieptNumber': reciept.recieptNumber
        })
      return Response(data)
    return Response({"message": "No purchase receipt found"}, status=status.HTTP_404_NOT_FOUND)