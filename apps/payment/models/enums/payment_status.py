from django.db import models


# TODO: (yoomoney) возможно много лишних статусов
class PaymentStatus(models.TextChoices):
    NEW = "new", "New"
    CANCELLED = "cancelled", "Cancelled"
    FAILED = "failed", "Failed"
    PENDING = "pending", "Pending"
    DECLINED = "declined", "Declined"
    REJECTED = "rejected", "Rejected"
    SUCCESS = "success", "Success"
