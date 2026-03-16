import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nearby_services.settings')
django.setup()

from services.models import Service

categories = [
    "Plumbing",
    "Electrical",
    "Cleaning",
    "Carpentry",
    "Painting",
    "Landscaping",
    "HVAC",
    "Pest Control",
    "Appliance Repair"
]

created_count = 0
for cat in categories:
    obj, created = Service.objects.get_or_create(
        name=cat, 
        defaults={'description': f'Professional {cat.lower()} services'}
    )
    if created:
        created_count += 1

print(f"Successfully created {created_count} service categories.")
