# libs
from celery import shared_task
# core
from apps.delivery.services.google_file_parser import google_file_to_dict
from apps.delivery.models import DeliveryZone, DeliveryZoneСoordinates, \
    DeliveryZoneFile
from apps.company.models import Institution
import logging
import os

app_logger = logging.getLogger('apps')


@shared_task
def google_map_file_upload_task(filename, pk):
    file = f'{os.getcwd()}{filename}'
    institution = Institution.objects.get(pk=pk)
    map_data = google_file_to_dict(file)

    for title, coordinates in map_data.items():
        # create delivery zones
        delivery_zone, delivery_zone_created = DeliveryZone.objects.get_or_create(
            institution=institution,
            title=title
        )
        # create map coordinates
        if delivery_zone_created is True:
            objs = [
                DeliveryZoneСoordinates(
                    zone=delivery_zone,
                    coordinates=i
                )
                for i in coordinates[0]
            ]
            DeliveryZoneСoordinates.objects.bulk_create(objs)
        else:
            # rm index from db & file that was uploaded
            DeliveryZoneFile.objects.get(institution=institution,
                                         file=filename[7:]).delete()
            os.remove(file)
            return 'Already exists'
