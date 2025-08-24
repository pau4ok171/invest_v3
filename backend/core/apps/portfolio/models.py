from django.db import models
from django.contrib.auth.models import User

from apps.invest.models import Instrument, Currency

class Portfolio(models.Model):
    name = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    positions = models.ManyToManyField(Instrument, through='PortfolioPosition')

    def __str__(self):
        return f'{self.user.id}:{self.name}'


class PortfolioPosition(models.Model):
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE)
    average_price = models.FloatField(null=True, blank=True)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, null=True, blank=True)
    share_amount = models.IntegerField(null=True, blank=True)

    class Meta:
        verbose_name = 'Portfolio Position'
        verbose_name_plural = 'Portfolio Positions'
