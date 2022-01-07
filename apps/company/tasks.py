# libs
from celery import shared_task
# core
from apps.base.services.salt_generator import create_salt_generator
from apps.company.services.custom_qr_image import create_qr_titles
from django.conf import settings
import os


@shared_task
def generate_qrcode_task(pk):
    from apps.company.models import Institution
    institution = Institution.objects.get(pk=pk)

    filepath = f'{settings.MEDIA_ROOT}/{institution.user.pk}/qrcode/'
    if os.path.exists(filepath) is False:
        os.makedirs(filepath)

    im_path = f'{filepath}{create_salt_generator(7)}_{institution.domain}.png'
    image = create_qr_titles(
        title1='МЕНЮ',
        title2='ОПЛАТА',
        title3='БОНУСЫ',
        domain=institution.domain
    )
    image.save(im_path)
    institution.qrcode = im_path
    institution.save()
