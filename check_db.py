import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nearby_services.settings')
django.setup()

from services.models import Service

services = Service.objects.all()
for s in services:
    print(f"ID: {s.id}, Name: {s.name}, Image: {s.image_url}")
