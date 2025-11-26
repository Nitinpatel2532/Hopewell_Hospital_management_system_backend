from django.urls import path
from . import views

from . views import Addpatient,patientLogin,patientdetils_crud_view,patientappointment,Sendotpview,Verifyotpview

urlpatterns = [
    path('addpatient/',Addpatient.as_view()),
    path('patientlogin/',patientLogin.as_view()),
    path('patient/<int:id>/',patientdetils_crud_view.as_view(),name='single-patient-crud'),
    path('patientappointment/', patientappointment.as_view(), name='patientappointment'),
    path('send-otp/',Sendotpview.as_view(),name="send_otp"),
    path('verify-otp/',Verifyotpview.as_view(),name='verify_otp')

]
