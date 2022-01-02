# libs
from celery import shared_task
# core
from apps.delivery.services.google_file_parser import google_file_to_dict
from apps.delivery.models import DeliveryZone, DeliveryZoneСoordinates
from apps.company.models import Institution


@shared_task
def google_map_file_upload_task(file, institution):
    map_data = google_file_to_dict(file)
    for title, coordinates in map_data.items():
        delivery_zone, delivery_zone_created = DeliveryZone.objects.get_or_create(
            institution=institution,
            title=title
        )
        if delivery_zone_created is True:
            objs = [
                DeliveryZoneСoordinates(
                    zone=delivery_zone,
                    coordinates=i
                )
                for i in coordinates[0]
            ]
            DeliveryZoneСoordinates.objects.bulk_create(objs)
