from django.db import models


class SeoModel(models.Model):
    """
    SEO Model with main params
    """
    title = models.CharField(blank=True, max_length=250, verbose_name='Title')
    description = models.CharField(blank=True, max_length=250, verbose_name='Description')
    keywords = models.CharField(blank=True, max_length=250, verbose_name='Keywords')
    h1 = models.CharField(blank=True, max_length=250, verbose_name='H1')

    def get_seo_title(self):
        if self.title:
            return self.title
        return ''

    def get_seo_description(self):
        if self.description:
            return self.description
        return ''

    def get_seo_keywords(self):
        if self.keywords:
            return self.keywords
        return ''

    def get_seo_h1(self):
        if self.h1:
            return self.h1
        return ''

    class Meta:
        abstract = True
