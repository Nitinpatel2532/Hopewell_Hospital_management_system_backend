from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import Superadminlogin
from .models import Superadmin_data
 

class Superadminloginview(APIView): 
    def post(self,request):
        serializer=Superadminlogin(data=request.data)
        if not serializer.is_valid():
             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        name=serializer.validated_data["name"]
        password=serializer.validated_data["psw"]
        try:
            user=Superadmin_data.objects.get(name=name)
        except Superadmin_data.DoesNotExist:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        if check_password(password, user.psw):
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

