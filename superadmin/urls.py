from django.urls import path

from .views import Superadminloginview
urlpatterns = [
    path('superlogin/',Superadminloginview.as_view(),name='superadmin-login')
] 