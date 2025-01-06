import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'daniels-hotell.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

username = 'admin10'
email = 'admin10@example.com'
password = 'admin10admin'

try:
    user = User.objects.get(username=username)
    user.email = email
    user.set_password(password)
    user.is_superuser = True
    user.is_staff = True
    user.save()
    print(f'Superuser {username} updated successfully!')
except User.DoesNotExist:
    User.objects.create_superuser(username, email, password)
    print(f'Superuser {username} created successfully!')
