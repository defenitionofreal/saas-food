from django.db import models
from apps.base.models.seo import SeoModel
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class Institution(SeoModel):
    """
    Institution(company) model
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    logo = models.ImageField(upload_to=f'images/users/', blank=True)  # images/users/self.user/institution/
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000, blank=True)
    phone = models.CharField(max_length=255)  # возможность добавить доп номер еще
    domen = models.CharField(max_length=255, unique=True)
    region = models.CharField(max_length=255)  # пакет вместо этого поля?
    city = models.CharField(max_length=255)  # пакет вместо этого поля?
    address = models.CharField(max_length=255) # пакет вместо этого поля?
    local_time = models.CharField(max_length=255)  # через что должно быть поле выбора местного времени, список?

    def __str__(self):
        return self.title


class Requisites(models.Model):
    """
    Institution paying requisites
    """
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    inn = models.IntegerField()
    kpp = models.IntegerField()
    ogrn = models.IntegerField()
    address = models.CharField(max_length=255)
    bank = models.CharField(max_length=255)
    bik = models.IntegerField()
    correspondent_account = models.IntegerField()
    checking_account = models.CharField(max_length=255)
    phone = models.CharField(max_length=255)  # списком
    email = models.EmailField()

    def __str__(self):
        return self.institution


class WorkingHours(models.Model):
    """
    Working time of institution
    """
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    weekday = models.CharField()  # choices
    from_hour = models.TimeField()
    to_hour = models.TimeField()

    def __str__(self):
        return self.institution


class Analytics(models.Model):
    """
    Analytics and metriks for institution
    """
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    yandex_metrika = models.CharField()
    google_analytics = models.CharField()
    google_tags = models.CharField()
    facebook_pixel = models.CharField()
    vk_pixel = models.CharField()
    tiktok_pixel = models.CharField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.institution


class SocialLinks(models.Model):
    """
    Links to other web apps
    """
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    instagram = models.CharField()
    vkontakte = models.CharField()
    facebook = models.CharField()
    youtube = models.CharField()
    tiktok = models.CharField()
    tripadvisor = models.CharField()

    def __str__(self):
        return self.institution


class Banner(models.Model):
    """
    Promo banners on the main page
    """
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='images/users/')  # images/users/self.user/banners/
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=1000)
    products = models.ForeignKey()  # products in a promo
    promo_code = models.ForeignKey()  # code in a promo
    link = models.CharField()
    link_text = models.CharField(max_length=100)

    def __str__(self):
        return f'{self.title} на {self.institution}'



class Design(models.Model):
    """
    Color of buttons and elements
    """
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)
    color = models.CharField(max_length=100)  # возможно использовать пакет для api colorfield?

    def __str__(self):
        return self.institution