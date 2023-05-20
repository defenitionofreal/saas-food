from django.db import models


class Status(models.IntegerChoices):
    ENQUEUED = 0, "В очереди"
    DELIVERED = 1, "Доставлено"
    FAILED = 2, "Не доставлено"
    SENT = 3, "Передано"
    WAITING = 4, "Ожидание статуса сообщения"
    DISMISSED = 6, "Отклонено"
    MODERATION = 8, "На модерации"
