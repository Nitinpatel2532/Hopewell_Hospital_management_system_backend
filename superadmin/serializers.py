from rest_framework import serializers

from .models import Superadmin_data

class Superadminlogin(serializers.Serializer):
    name=serializers.CharField()
    psw=serializers.CharField()