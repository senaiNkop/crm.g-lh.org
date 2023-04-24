from django.conf import settings
from django.contrib import admin
from django.db import models

from django.urls import reverse
from django.utils import timezone

import pandas as pd


DEFAULT = 0
STATUS = (
    ('completed', 'Completed'),
    ('in_progress', 'In Progress'),
    ('not_started', 'Not Started')
)


class DataAnalysisManager(models.Manager):
    # def get_queryset(self):
    #     return super(DataAnalysisManager, self).get_queryset().filter(username=settings.AUTH_USER_MODEL)

    def date_series(self, user) -> pd.DatetimeIndex:
        object = self.get_queryset().filter(username=user).values_list('date', flat=True)

        return pd.to_datetime(object)


# Create your models here.
class BibleReading(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='username')
    date = models.DateField(default=timezone.now)

    bible_passage = models.CharField(max_length=100)
    status = models.CharField(max_length=50, choices=STATUS)
    comment = models.TextField()

    objects = models.Manager()
    data_analysis = DataAnalysisManager()

    def __str__(self):
        return f"{self.bible_passage} - {self.status}"

    def get_absolute_url(self):
        return reverse('bible_reading:detail',
                       args=[self.bible_passage, self.id])

    class Meta:
        ordering = ('-date', )


class PrayerMarathon(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='username')
    comment = models.TextField()
    date = models.DateField(default=timezone.now)

    objects = models.Manager()
    data_analysis = DataAnalysisManager()

    def __str__(self):
        return f"Prayer Marathon on {self.date.strftime('%a %d %b %Y')}"

    @admin.display(description="Comment")
    def trunc_comment(self):
        return f"{self.comment[:20]}..."

    def get_absolute_url(self):
        return reverse('prayer_marathon:detail', args=[self.id])

    class Meta:
        ordering = ('-date',)
