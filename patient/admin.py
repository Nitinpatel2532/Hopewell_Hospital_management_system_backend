from django.contrib import admin
from .models import Patient_signup,patient_appointment

# Register your models here.

@admin.register(Patient_signup)
# admin.site.register(Patient_signup)

class patientdata(admin.ModelAdmin):
    list_display=['First_name','Last_name','Contact_number','Email']

@admin.register(patient_appointment)
class patientappointment(admin.ModelAdmin):
    list_display=['patient','date','blood_group','department','address',]
