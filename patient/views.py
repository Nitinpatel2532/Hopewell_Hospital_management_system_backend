from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .serializers import patientsignupapi, patientappointmentapi
from .models import Patient_signup, Emailotp
from .utils import create_otp, send_otp_email
from django.utils import timezone



class Addpatient(APIView):
    def post(self, request):
        serializer = patientsignupapi(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Patient added successfully'}, status=201)
        return Response(serializer.errors, status=400)

    def get(self, request):
        patients = Patient_signup.objects.all()
        serializer = patientsignupapi(patients, many=True)
        return Response(serializer.data, status=200)


class patientLogin(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('psw')

        try:
            patient = Patient_signup.objects.get(Email=email)

            if patient.password == password:
                return Response({
                    'message': "Login Successfully",
                    'id': patient.id,
                    'fname': patient.First_name,
                    'lname': patient.Last_name,
                    'Email': patient.Email,
                    'mobile': patient.Contact_number,
                    'password': patient.password,
                }, status=200)

            return Response({'message': "Invalid Password"}, status=401)

        except Patient_signup.DoesNotExist:
            return Response({'message': "User not found"}, status=404)


class patientdetils_crud_view(generics.RetrieveUpdateDestroyAPIView):
    queryset = Patient_signup.objects.all()
    serializer_class = patientsignupapi
    lookup_field = 'id'


class patientappointment(APIView):
    def post(self, request):
        serializer = patientappointmentapi(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': "Appointment created successfully"}, status=201)
        return Response(serializer.errors, status=400)


# =============================
#   OTP VIEWS (WORKING)
# =============================

from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Patient_signup, Emailotp
from .utils import create_otp, send_otp_email
from django.utils import timezone

@method_decorator(csrf_exempt, name='dispatch')
class Sendotpview(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            if not email:
                return Response({'error': 'Email required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = Patient_signup.objects.get(Email=email)
            except Patient_signup.DoesNotExist:
                return Response({'error': 'Email not registered'}, status=status.HTTP_400_BAD_REQUEST)

            otp = create_otp(user)
            # send_otp_email returns None normally but will raise if fail
            send_otp_email(user, otp)
            return Response({'message': 'OTP sent successfully'}, status=status.HTTP_200_OK)

        except Exception as e:
            # helpful during debugging — remove or log in production
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class Verifyotpview(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            otp = request.data.get('otp')
            if not email or not otp:
                return Response({'error': 'Email and otp required'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = Patient_signup.objects.get(Email=email)
            except Patient_signup.DoesNotExist:
                return Response({'error': 'User not found'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                otp_obj = Emailotp.objects.filter(user=user, otp=otp).latest('created_at')
            except Emailotp.DoesNotExist:
                return Response({'error': 'Invalid OTP'}, status=status.HTTP_400_BAD_REQUEST)

            if timezone.now() <= otp_obj.valid_untill:
                user.is_verified = True
                user.save()
                return Response({'message': 'OTP verified successfully'}, status=status.HTTP_200_OK)
            else:
                return Response({'error': 'OTP expired'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
