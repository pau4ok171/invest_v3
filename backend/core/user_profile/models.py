from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

from invest.models import Country, Currency, Company
from notes.models import Note
from portfolio.models import Portfolio


STOCK_VIEW_CHOICES = (
    ('table', 'Table View'),
    ('tile', 'Tile View'),
)

THEME_CHOICES = (
    ('finargo-light', 'Finargo Light'),
    ('finargo-dark', 'Finargo Dark'),
)


def get_portfolio_path(instance, filename):
    return f'profiles/avatars/{instance.user.id}/{filename}'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    display_name = models.CharField(max_length=100, null=True)
    avatar = models.ImageField(null=True, blank=True, upload_to=get_portfolio_path)
    locale = models.CharField(max_length=10, default='en')
    country = models.ForeignKey(Country, on_delete=models.PROTECT, default=2)
    currency = models.ForeignKey(Currency, on_delete=models.PROTECT, default=1)
    auth_provider = models.CharField(max_length=50, default='email')
    bio = models.TextField(max_length=240, null=True)
    external_link = models.URLField(null=True, blank=True)
    watchlisted_companies = models.ManyToManyField(Company, blank=True, related_name='profile_companies')
    portfolios = models.ManyToManyField(Portfolio, blank=True, related_name='profile_portfolios')
    stock_view = models.CharField(default='table', max_length=50, choices=STOCK_VIEW_CHOICES)
    theme = models.CharField(default='finargo-light', max_length=50, choices=THEME_CHOICES)
    banner_color = models.CharField(default='#FFFFFF', max_length=7)

    def __str__(self):
        return f"Profile of {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if hasattr(instance, 'profile'):
        instance.profile.save()
