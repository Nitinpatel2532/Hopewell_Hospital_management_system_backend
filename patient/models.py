from django.db import models
from datetime import datetime
from django.utils import timezone

# Create your models here.

class Patient_signup(models.Model):
    First_name=models.CharField(max_length=50)
    Last_name=models.CharField(max_length=50)
    Contact_number = models.CharField(max_length=15)

    Email=models.EmailField(max_length=254,unique=True)
    password=models.CharField(max_length=50)
    is_verified=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.First_name

class Emailotp(models.Model):
    user=models.ForeignKey(Patient_signup,on_delete=models.CASCADE)
    otp=models.CharField(max_length=6)
    created_at=models.DateTimeField(auto_now_add=True)
    valid_untill=models.DateTimeField()

    def is_valid(self):
        return timezone.now() <= self.valid_untill


class patient_appointment(models.Model):
    blood=[
    ('A+', 'A+ (A Positive)'),
    ('A-', 'A- (A Negative)'),
    ('B+', 'B+ (B Positive)'),
    ('B-', 'B- (B Negative)'),
    ('AB+', 'AB+ (AB Positive)'),
    ('AB-', 'AB- (AB Negative)'),
    ('O+', 'O+ (O Positive)'),
    ('O-', 'O- (O Negative)'),
]

    dept=[
        ('Cardiology','Cardiology'),
        ('Neurology','Neurology'),
        ('Orthopedics','Orthopedics'),
        ('Pediatrics','Pediatrics'),
        ('Gynecology','Gynecology'),
        ('Dermatology','Dermatology'),
        ('Urology','Urology'),
        ('ENT','ENT'),
        ('Radiology','Radiology'),
        ('Emergency Medicine','Emergency Medicine'),
        ('General Surgery','General Surgery'),
        ('Nephrology','Nephrology'),
        ('Gastroenterology','Gastroenterology'),
        ('Pulmonology','Pulmonology'),
        ('Ophthalmology','Ophthalmology'),
        ('Psychiatry','Psychiatry'),
        ('Pathology','Pathology'),
        ('Dentistry','Dentistry'),
        ('Physiotherapy / Rehabilitation','Physiotherapy / Rehabilitation'),
        ('Obstetrics','Obstetrics'),
        ('Endocrinology','Endocrinology'),
    ]
    patient=models.ForeignKey(Patient_signup,on_delete=models.CASCADE)
    date=models.DateField(default=datetime.now)
    blood_group=models.CharField(max_length=128,choices=blood)
    department=models.CharField(max_length=128,choices=dept)
    address=models.CharField(max_length=128)

    def __str__(self):
        return self.patient.Email
