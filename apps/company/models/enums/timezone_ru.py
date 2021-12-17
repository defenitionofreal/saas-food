from django.db import models


class RussianTimezone(models.TextChoices):
    MOSCOW = "moscow", "UTC+3"
    KALININGRAD = "kaliningrad", "UTC+2"
    SAMARA = "samara", "UTC+4"
    YEKATERINBURG = "yekaterinburg", "UTC+5"
    OMSK = "omsk", "UTC+6"
    KRASNOYARSK = "krasnoyarsk", "UTC+7"
    NOVOSIBIRSK = "novosibirsk", "UTC+7"
    IRKUTSK = "irkutsk", "UTC+8"
    YAKUTSK = "Yakutsk", "UTC+9"
    VLADIVOSTOK = "vladivostok", "UTC+10"
    MAGADAN = "Magadan", "UTC+11"
    SAKHALIN = "Sakhalin", "UTC+11"
    SREDNEKOLYMSK = "Srednekolymsk", "UTC+11"
    ANADYR = "Anadyr", "UTC+12"
    KAMCHATKA = "Kamchatka", "UTC+12"
