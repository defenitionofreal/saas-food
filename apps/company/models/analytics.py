from django.db import models


class Analytics(models.Model):
    """
    Analytics and metrics for institution
    """
    institution = models.ForeignKey("company.Institution", on_delete=models.CASCADE, related_name="analytics")
    yandex_metrics = models.TextField()
    google_analytics = models.TextField()
    google_tags = models.TextField()
    facebook_pixel = models.TextField()
    vk_pixel = models.TextField()
    tiktok_pixel = models.TextField()
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.institution}"
