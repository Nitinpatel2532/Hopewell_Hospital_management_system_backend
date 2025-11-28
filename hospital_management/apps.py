from django.apps import AppConfig


class HospitalManagementConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hospital_management'


from django.apps import AppConfig
import os

class HospitalConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'hospital'

    def ready(self):
        # Run admin creation only if environment variable is set
        if os.environ.get("RUN_ADMIN_SETUP") == "True":
            from django.db import connection
            if connection.settings_dict['ENGINE']:
                from create_admin import create_super_user
                create_super_user()
