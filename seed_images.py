import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nearby_services.settings')
django.setup()

from services.models import Service

# Mapping of categories to Unsplash/professional image URLs
image_mapping = {
    "Plumbing": "https://images.unsplash.com/photo-1585704032915-c3400ca199e7?q=80&w=600&auto=format&fit=crop",
    "Electrical": "https://images.unsplash.com/photo-1621905251189-08b45d6a269e?q=80&w=600&auto=format&fit=crop",
    "Cleaning": "https://images.unsplash.com/photo-1581578731548-c64695cc6952?q=80&w=600&auto=format&fit=crop",
    "Carpentry": "https://images.unsplash.com/photo-1505015920881-0f83c2f7c95e?q=80&w=600&auto=format&fit=crop",
    "Painting": "https://images.unsplash.com/photo-1589939705384-5185137a7f0f?q=80&w=600&auto=format&fit=crop",
    "Landscaping": "https://images.unsplash.com/photo-1588607736345-4de4b6f14548?q=80&w=600&auto=format&fit=crop",
    "HVAC": "https://images.unsplash.com/photo-1594956334237-640a2bb128d5?q=80&w=600&auto=format&fit=crop",
    "Pest Control": "https://images.unsplash.com/photo-1610408542939-ebd71ceae06b?q=80&w=600&auto=format&fit=crop",
    "Appliance Repair": "https://images.unsplash.com/photo-1581092160562-40aa08e78837?q=80&w=600&auto=format&fit=crop"
}

updated_count = 0
for name, url in image_mapping.items():
    service = Service.objects.filter(name=name).first()
    if service:
        service.image_url = url
        service.save()
        updated_count += 1

print(f"Successfully updated {updated_count} service categories with images.")
