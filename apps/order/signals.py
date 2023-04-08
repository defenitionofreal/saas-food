from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.order.models.cart import Cart
from apps.order.models.enums.order_status import OrderStatus

from apps.que.models import Que
from apps.que.models.enums.que_status import QueStatus


@receiver(post_save, sender=Cart)
def order_que_receiver(sender, instance, **kwargs):
    """
    Changing queue status.
    Depends on status of an order.
    """
    # TODO: celery task
    if instance.status == OrderStatus.PLACED:
        Que.objects.get_or_create(order_id=instance.id,
                                  status=QueStatus.PROCESSING)
    if instance.status == OrderStatus.ACCEPTED:
        Que.objects.get_or_create(order_id=instance.id,
                                  status=QueStatus.ACCEPTED)
    if instance.status == OrderStatus.COOKING:
        Que.objects.get_or_create(order_id=instance.id,
                                  status=QueStatus.COOKING)
    if instance.status == OrderStatus.READY:
        Que.objects.get_or_create(order_id=instance.id,
                                  status=QueStatus.READY)
    if instance.status == OrderStatus.CANCELED:
        Que.objects.get_or_create(order_id=instance.id,
                                  status=QueStatus.CANCELED)
