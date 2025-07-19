from django.db import models
from invest import models as invest_models
from django.contrib.auth.models import User


class Portfolio(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    positions = models.ManyToManyField(invest_models.Company, through='PortfolioCompany')

    def __str__(self):
        return f'{self.user.id}:{self.name}'


class PortfolioCompany(models.Model):
    company = models.ForeignKey(invest_models.Company, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    average_price = models.FloatField(null=True, blank=True)
    currency = models.ForeignKey(invest_models.Currency, on_delete=models.PROTECT, null=True, blank=True)
    share_amount = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Portfolio Company'
        verbose_name_plural = 'Portfolio Companies'
