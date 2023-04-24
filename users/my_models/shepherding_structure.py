import datetime

from django.db import models
from django.contrib import admin
from django.contrib.auth import get_user_model

from .utilities import ValidationError, Validators


Calling = (
    ('unknown', 'Unknown'),
    ('apostle', 'Apostle'),
    ('prophet', 'Prophet'),
    ('evangelist', 'Evangelist'),
    ('teacher', 'Teacher'),
    ('pastor', 'Pastor'),
)


class Shepherd(models.Model):
    name = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, to_field='username',
                                related_name='+', limit_choices_to={'is_staff': True})
    no_of_sheep = models.IntegerField()
    date_of_appointment = models.DateField(validators=[Validators.validate_prevent_future_date])
    calling = models.CharField(max_length=15, default='unknown', choices=Calling)

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ('no_of_sheep', )

    @admin.display(ordering='date_of_appointment', description='Duration of Service')
    def get_service_duration(self):
        if self.date_of_appointment:
            now = datetime.date.today()

            duration = now - self.date_of_appointment
            duration_year = duration.days // 365
            duration_days = duration.days % 365

            return f"{duration_year} year {duration_days} days"
        else:
            raise ValueError("Date of appointment must be set")

    @admin.display(description="Full name")
    def get_shepherd_full_name(self):
        return str(self.name)

    @admin.display(description='Sex')
    def get_shepherd_gender(self):
        return self.name.gender

    def set_date_of_appointment(self, date):
        date = Validators.validate_prevent_future_date(value=date)

        self.date_of_appointment = date


class SubShepherd(models.Model):
    name = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, to_field='username')
    no_of_sheep = models.IntegerField()
    date_of_appointment = models.DateField(validators=[Validators.validate_prevent_future_date])
    calling = models.CharField(max_length=15, choices=Calling)

    def __str__(self):
        return self.get_subshepherd_full_name()

    class Meta:
        ordering = ('no_of_sheep', )
        verbose_name = "Sub Shepherd"

    @admin.display(ordering='date_of_appointment', description='Duration of Service')
    def get_service_duration(self):
        if self.date_of_appointment:
            now = datetime.date.today()

            duration = now - self.date_of_appointment
            duration_year = duration.days // 365
            duration_days = duration.days % 365

            return f"{duration_year} year {duration_days} days"
        else:
            raise ValueError("Date of appointment must be set")

    @admin.display(description="Full name")
    def get_subshepherd_full_name(self):
        return str(self.name)

    @admin.display(description='Sex')
    def get_subshepherd_gender(self):
        return self.name.gender

    @admin.display(description='Shepherd')
    def get_shepherd_full_name(self):
        return f"{self.shepherd.name.first_name} {self.shepherd.name.last_name}"

    def clean(self):
        # Don't let sub shepherd be the shepherd of himself
        shepherd = self.shepherd.name.username
        sub_shepherd = self.name.username

        if shepherd == sub_shepherd:
            raise ValidationError(_("A Sub Shepherd can't also be his own Shepherd"))

    def set_date_of_appointment(self, date):
        date = Validators.validate_prevent_future_date(value=date)

        self.date_of_appointment = date
