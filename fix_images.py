import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nearby_services.settings')
django.setup()

from services.models import Service

# Use beautiful, fitting Unsplash images
images_to_update = {
    "Painting": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?q=80&w=600&auto=format&fit=crop",
    "Landscaping": "https://images.unsplash.com/photo-1558904541-efa843a96f0f?q=80&w=600&auto=format&fit=crop"
}

updated = 0
for name, url in images_to_update.items():
    service = Service.objects.filter(name__icontains=name).first()
    if service:
        service.image_url = url
        service.save()
        print(f"Updated image for {service.name}")
        updated += 1
    else:
        print(f"Service {name} not found")

print(f"Total updated: {updated}")
