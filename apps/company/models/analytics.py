from django.db import models


class Analytics(models.Model):
    """
    Analytics and metrics for institution
    """
    institution = models.ForeignKey(
        "company.Institution",
        on_delete=models.CASCADE,
        related_name="analytics"
    )
    yandex_metrics = models.CharField(max_length=100, blank=True)  # 48848231
    google_analytics = models.CharField(max_length=100, blank=True)  # UA-120268648-1
    google_tags = models.CharField(max_length=100, blank=True)  # GTM-TPTV57W
    facebook_pixel = models.CharField(max_length=100, blank=True)  # 554789992564123
    vk_pixel = models.CharField(max_length=100, blank=True)  # VK-RTRG-289274-732uW
    tiktok_pixel = models.CharField(max_length=100, blank=True)  # BQWIWUU
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.institution}"
