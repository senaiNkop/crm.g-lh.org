
from datetime import date

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


CHOICES = (
    ('prayer_marathon', 'Prayer Marathon'),
    ('bible_reading', 'Bible Reading'),
    ('church_work', 'Church Work'),
    ('evangelism', 'Evangelism'),
    ('prophetic_vision', 'Prophetic Vision'),
    ('bio_data', 'Bio Data')
)


class RecentActivityManager(models.Manager):
    def auto_delete_old_activities(self, username):
        all_activities = self.get_queryset().filter(username=username).order_by('date')
        old_activities = all_activities[10:]
        new_activities = all_activities[:10]

        if old_activities:
            for activity in old_activities:
                activity.delete()

        return new_activities


class RecentActivity(models.Model):
    username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, to_field='username')
    category = models.CharField(max_length=20, choices=CHOICES)
    date = models.DateField(auto_now_add=True)
    details = models.CharField(max_length=100, blank=True, null=True)

    objects = models.Manager()
    custom_objects = RecentActivityManager()

    def __str__(self):
        return f"{self.category} on {self.date}"

    class Meta:
        ordering = ('-date', )
        verbose_name_plural = "Recent Activities"
