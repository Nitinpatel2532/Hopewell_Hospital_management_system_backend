from rest_framework import serializers

from . models import Patient_signup,patient_appointment

class patientsignupapi(serializers.ModelSerializer):
    class Meta:
        model=Patient_signup
        fields='__all__'


class patientappointmentapi(serializers.ModelSerializer):
    class Meta:
        model=patient_appointment
        fields='__all__'
