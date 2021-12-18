from django.db import models


class SeoModel(models.Model):
    """
    SEO Model with main params
    """
    seo_title = models.CharField(blank=True, max_length=250, verbose_name='Title')
    seo_description = models.CharField(blank=True, max_length=250, verbose_name='Description')
    seo_keywords = models.CharField(blank=True, max_length=250, verbose_name='Keywords')
    seo_h1 = models.CharField(blank=True, max_length=250, verbose_name='H1')

    def get_seo_title(self):
        if self.seo_title:
            return self.seo_title
        return ''

    def get_seo_description(self):
        if self.seo_description:
            return self.seo_description
        return ''

    def get_seo_keywords(self):
        if self.seo_keywords:
            return self.seo_keywords
        return ''

    def get_seo_h1(self):
        if self.seo_h1:
            return self.seo_h1
        return ''

    class Meta:
        abstract = True
