from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt

from .serializers import patientsignupapi, patientappointmentapi
from .models import Patient_signup, Emailotp
from .utils import create_otp, send_otp_email


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

@method_decorator(csrf_exempt, name='dispatch')
class Sendotpview(APIView):
    def post(self, request):
        email = request.data.get('email')

        if not email:
            return Response({'error': 'Email required'}, status=400)

        try:
            user = Patient_signup.objects.get(Email=email)
        except Patient_signup.DoesNotExist:
            return Response({'error': 'Email not registered'}, status=400)

        otp = create_otp(user)
        sent = send_otp_email(user, otp)

        if not sent:
            return Response({'error': 'Failed to send OTP'}, status=500)

        return Response({'message': 'OTP sent successfully'}, status=200)


@method_decorator(csrf_exempt, name='dispatch')
class Verifyotpview(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp = request.data.get('otp')

        if not email or not otp:
            return Response({'error': 'Email and OTP required'}, status=400)

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

        return Response({'error': 'OTP expired'}, status=400)
