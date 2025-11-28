from django.contrib.auth.models import User

def create_super_user():
    try:
        if not User.objects.filter(username="admin").exists():
            User.objects.create_superuser(
                username="admin",
                email="admin@example.com",
                password="Admin@123"
            )
            print("Superuser 'admin' created successfully!")
        else:
            print("Superuser already exists.")
    except Exception as e:
        print("Error creating superuser:", e)
