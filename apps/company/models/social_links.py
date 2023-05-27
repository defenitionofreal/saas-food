from django.db import models


class SocialLinks(models.Model):
    """
    Links to other web apps
    """
    institution = models.ForeignKey(
        "company.Institution",
        on_delete=models.CASCADE,
        related_name="social_links"
    )
    instagram = models.CharField(max_length=100, blank=True)  # @nickname
    vkontakte = models.CharField(max_length=100, blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    youtube = models.CharField(max_length=100, blank=True)
    tiktok = models.CharField(max_length=100, blank=True)
    tripadvisor = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.institution}"
