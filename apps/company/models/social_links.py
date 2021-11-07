from django.db import models


class SocialLinks(models.Model):
    """
    Links to other web apps
    """
    institution = models.ForeignKey("apps.company.Institution", on_delete=models.CASCADE, related_name="social_links")
    instagram = models.URLField()
    vkontakte = models.URLField()
    facebook = models.URLField()
    youtube = models.URLField()
    tiktok = models.URLField()
    tripadvisor = models.URLField()

    def __str__(self):
        return f"{self.institution}"
