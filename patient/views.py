from django.shortcuts import render,HttpResponse
from rest_framework .views import APIView
from rest_framework.response import Response
from rest_framework import status,generics
from .serializers import patientsignupapi,patientappointmentapi
from .models import Patient_signup,Emailotp
from .utils import create_otp,send_otp_email

# Create your views

class Addpatient(APIView):
    def post(self,request):
        serializer=patientsignupapi(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message':'Patient added successfully'},status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def get(self,request):
        patients = Patient_signup.objects.all()
        serializer = patientsignupapi(patients, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class patientLogin(APIView):
    def post(self,request):
        email_field=request.data.get('email')
        password_field=request.data.get('psw')
        print(email_field,password_field)
        try:
            patient=Patient_signup.objects.get(Email=email_field)
            if patient.password==password_field:
                return Response(
                    {
                        'message':"Login Successfully",
                        'id':patient.id,
                        'fname':patient.First_name,
                        'lname':patient.Last_name,
                        'Email':patient.Email,
                        'mobile':patient.Contact_number,
                        'password':patient.password,

                    },status=status.HTTP_200_OK
                )
            else:
                return Response({'message':"Invalid Password"},status=status.HTTP_401_UNAUTHORIZED)
        except Patient_signup.DoesNotExist:
            return Response({'message':"User not found"},status=status.HTTP_404_NOT_FOUND)


class patientdetils_crud_view(generics.RetrieveUpdateDestroyAPIView):
    queryset=Patient_signup.objects.all()
    serializer_class=patientsignupapi
    lookup_field='id'


class patientappointment(APIView):
    def post(self,request):
        serializer=patientappointmentapi(data=request.data)
        print(request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response({'message':"Appointment created succesfully"},status=status.HTTP_201_CREATED)
        print(serializer.errors)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        
        
# class Sendotpview(APIView):
#     def post(self,request):
#         email=request.data.get('email')
#         user,create=Patient_signup.objects.get_or_create(Email=email)
#         otp=create_otp(user)
#         send_otp_email(user,otp)
#         return Response({'message':'otp_sent'},status=200)

class Sendotpview(APIView):
    def post(self, request):
        email = request.data.get('email')

        # Email must already exist
        try:
            user = Patient_signup.objects.get(Email=email)
        except Patient_signup.DoesNotExist:
            return Response({'error': 'Email not registered'}, status=400)

        # Create OTP
        otp = create_otp(user)
        send_otp_email(user, otp)

        return Response({'message': 'OTP sent successfully'}, status=200)

    

# class Verifyotpview(APIView):
#     def post(self,request):
#         email=request.data.get('email')
#         otp=request.data.get('otp')

#         try:
#             user=Patient_signup.objects.get(Email=email)
#             otp_obj=Emailotp.objects.filter(user=user,otp=otp).latest('created_at')
#             if otp_obj.is_valid():
#                 user.is_verified=True
#                 user.save()
#                 return Response({'message':'verify'},status=200)
#             else:
#                 return Response({'message':'expired otp'},status=400)
        
#         except Patient_signup.DoesNotExist:
#             return Response({'message':'User does not found'},status=400)
#         except Emailotp.DoesNotExist:
#             return Response({'error':'Invalid otp'},status=400)

class Verifyotpview(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        try:
            user = Patient_signup.objects.get(Email=email)
        except Patient_signup.DoesNotExist:
            return Response({'error': 'User not found'}, status=400)

        try:
            otp_obj = Emailotp.objects.filter(user=user, otp=otp).latest('created_at')
        except Emailotp.DoesNotExist:
            return Response({'error': 'Invalid OTP'}, status=400)

        if otp_obj.is_valid():
            user.is_verified = True
            user.save()
            return Response({'message': 'OTP verified'}, status=200)
        else:
            return Response({'error': 'OTP expired'}, status=400)
