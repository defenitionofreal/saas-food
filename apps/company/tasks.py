# libs
from celery import shared_task
# core
from apps.base.services.salt_generator import create_salt_generator
from apps.company.services.custom_qr_image import create_qr_titles
from django.core.files.base import ContentFile
from io import BytesIO


@shared_task
def generate_qrcode_task(pk):
    from apps.company.models import Institution
    institution = Institution.objects.get(pk=pk)
    im_name = f"{create_salt_generator(7)}_{institution.domain}.png"
    image = create_qr_titles(
        title1='МЕНЮ',
        title2='ОПЛАТА',
        title3='БОНУСЫ',
        domain=institution.domain
    )
    byte_io = BytesIO()
    image.save(byte_io, 'PNG')
    institution.qrcode.save(im_name,
                            ContentFile(byte_io.getvalue()),
                            save=True)
