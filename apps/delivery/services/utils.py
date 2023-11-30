from typing import Optional

from django.db.models import Count, Max

from apps.delivery.models import CustomerAddress, DeliveryTypeRule, DeliveryZone

from turfpy.measurement import boolean_point_in_polygon
from geojson import Point, Polygon
from django.utils import timezone

import json


def get_order_date(cls, order_date: str):
    # todo: localize to an affiliate timezone ?
    date = order_date
    if date is None or date == "":
        date = timezone.now()
    return date


def merge_customer_address(session_key: str, user_id: int):
    """
    Merge address from session to user after authentication
    """
    CustomerAddress.objects.filter(
        user__isnull=True, session_id=session_key
    ).update(user_id=user_id)


def delete_customer_last_duplicated_addresses(user_id: int):
    """
    Delete last customer address duplicates at field - display_name
    """
    duplicate_ids = CustomerAddress.objects.filter(
        user_id=user_id).values('display_name').annotate(
        duplicate=Count('display_name'), last_id=Max('id')).filter(
        duplicate__gt=1).values_list('last_id', flat=True)
    CustomerAddress.objects.filter(
        user_id=user_id, id__in=duplicate_ids
    ).delete()


def get_delivery_type_rule(delivery_type: str,
                           institution_id: str) -> Optional[DeliveryTypeRule]:
    """ """
    delivery_type_rule = DeliveryTypeRule.objects.filter(
        institutions__id=institution_id,
        delivery_type=delivery_type,
        is_active=True
    ).first()
    return delivery_type_rule


def has_zones_and_delivery_zone_object(institution: object, latitude: str, longitude: str) -> tuple:
    """ """
    active_zones = institution.deliveryzone_set.filter(is_active=True)
    is_any_active_zone_exists = active_zones.exists()
    zone_obj = None
    point = Point((float(longitude), float(latitude)))
    for zone in active_zones:
        if boolean_point_in_polygon(point, Polygon(json.loads(zone.coordinates))):
            zone_obj = zone
            break

    return is_any_active_zone_exists, zone_obj
