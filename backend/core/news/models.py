from django.db import models


class News(models.Model):
    company = models.ForeignKey('invest.Company', related_name='company_news', on_delete=models.CASCADE)
    type = models.CharField(
        max_length=255,
        choices={'DIVIDEND': 'dividend', 'UPDATE': 'update', 'ACTION': 'corporate action'}
    )
    date = models.DateField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = 'News'
        verbose_name_plural = 'News'
        ordering = ['-date']
