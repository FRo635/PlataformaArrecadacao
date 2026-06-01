from django.db import models
from django.utils import timezone


class Campaign(models.Model):
    title = models.CharField(max_length=160)
    org = models.CharField(max_length=160)
    desc = models.TextField()
    goal = models.DecimalField(max_digits=12, decimal_places=2)
    deadline = models.DateField()

    def __str__(self):
        return self.title


class Allocation(models.Model):
    campaign = models.ForeignKey(Campaign, related_name='allocations', on_delete=models.CASCADE)
    name = models.CharField(max_length=120)
    pct = models.PositiveSmallIntegerField()

    def __str__(self):
        return f'{self.campaign}: {self.name}'


class SpendLog(models.Model):
    campaign = models.ForeignKey(Campaign, related_name='spend_logs', on_delete=models.CASCADE)
    date = models.DateField()
    cat = models.CharField(max_length=120)
    desc = models.CharField(max_length=240, blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)

    class Meta:
        ordering = ['-date', '-id']


class DonorUser(models.Model):
    name = models.CharField(max_length=160)
    email = models.EmailField(unique=True)
    password_hash = models.CharField(max_length=256)
    role = models.CharField(max_length=40, default='donor')

    def __str__(self):
        return self.email


class Donation(models.Model):
    campaign = models.ForeignKey(Campaign, related_name='donations', on_delete=models.CASCADE)
    user = models.ForeignKey(DonorUser, related_name='donations', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    date = models.DateField(default=timezone.localdate)
    anonymous = models.BooleanField(default=False)

    class Meta:
        ordering = ['-date', '-id']
