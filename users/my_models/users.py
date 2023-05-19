import datetime

from django.db import models
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


from .utilities import Validators, ValidationError, get_user_name


SEX_CHOICES = (
    ('M', "Male"),
    ('F', "Female")
)


BLOOD_GROUP_CHOICES = (
    ('-', 'Unknown'),
    ('A+', 'A+'),
    ('A-', 'A-'),
    ('B+', 'B+'),
    ('B-', 'B-'),
    ('AB+', 'AB-'),
    ('O+', 'O+'),
    ('O-', 'O-')
)


GENOTYPE_CHOICES = (
    ('-', 'Unknown'),
    ('AA', 'AA'),
    ('AB', 'AB'),
    ('AO', 'AO'),
    ('BB', 'BB'),
    ('BO', 'BO'),
    ('OO', 'OO'),
    ('AS', 'AS'),
    ('SS', 'SS')
)

LEVEL_CHOICES = (
    ('new_mem', 'New Member'),
    ('mem', 'Member'),
    ('worker', 'Worker'),
    ('sub_shep', 'Sub Shepherd'),
    ('core_shep', 'Core Shepherd'),
    ('chief_shep', 'Chief Shepherd')
)


# Create your models here.
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, save=True, **extra_fields):
        """Create and save a user with the given email and password"""
        if not email:
            raise ValueError(_("The email must be set"))

        if 'date_of_birth' in extra_fields:
            dob = extra_fields['date_of_birth']
            Validators.validate_prevent_future_date(dob)

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        if save:
            user.save()

        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a super user with the given email and password"""
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError(_("Superuser must have is_staff=True"))
        if extra_fields.get("is_superuser") is not True:
            raise ValueError(_("Superuser must have is_superuser=True"))

        return self.create_user(email, password, **extra_fields)

    def get_sheep(self, shepherd):
        return self.get_queryset().filter(shepherd=shepherd)

    def get_sub_sheep(self, sub_shepherd):
        return self.get_queryset().filter(sub_shepherd=sub_shepherd)


class CustomUser(AbstractUser):

    # BIO DATA
    first_name = models.CharField(_('First Name'), max_length=100)
    last_name = models.CharField(_('Last Name'), max_length=100)
    username = models.CharField(_('Username'), max_length=100, unique=True)
    gender = models.CharField(_('Gender'), max_length=2, choices=SEX_CHOICES)
    date_of_birth = models.DateField(_("Date of Birth"), blank=True, null=True,
                                     validators=[Validators.validate_prevent_future_date])
    about = models.TextField(_("About"), blank=True, null=True)
    profile_pic = models.FileField(_("Profile pic"), upload_to=get_user_name, blank=True)

    # PERSONAL DATA
    phone_number = models.CharField(_("Phone Number"), max_length=20)
    email = models.EmailField(_("Email address"), unique=True)
    occupation = models.CharField(_('Occupation'), max_length=100, blank=True, null=True)
    address = models.CharField(_("Address"), max_length=500)
    skills = models.CharField(_('Skills'), max_length=1000, blank=True, null=True)

    # BASIC MEDICAL INFORMATION
    blood_group = models.CharField(_("Blood Group"), max_length=10, choices=BLOOD_GROUP_CHOICES)
    genotype = models.CharField(_("Genotype"), max_length=10, choices=GENOTYPE_CHOICES)
    chronic_illness = models.CharField(_("Any Chronic Ailment"), max_length=100, help_text="please specify", blank=True, null=True)

    # RESIDENTIAL INFORMATION
    lga = models.CharField(_("LGA"), max_length=300, blank=True, null=True)
    state = models.CharField(_("State"), max_length=100, blank=True, null=True)
    country = models.CharField(_("Country"), max_length=100, blank=True, null=True)

    # SCHOOL INFORMATION
    course_of_study = models.CharField(_("Course of Study"), max_length=255, blank=True, null=True)
    years_of_study = models.IntegerField(_("No of Years of Study"), blank=True, null=True)
    current_year_of_study = models.IntegerField(_("Current Year of Study"), blank=True, null=True)
    final_year_status = models.CharField(_("Final Year Status"), max_length=20, help_text=_("Update when appropriate"), blank=True, null=True)

    # NEXT OF KIN INFORMATION
    next_of_kin_full_name = models.CharField(_('Full Name'), max_length=200, blank=True, null=True)
    next_of_kin_relationship = models.CharField(_('Relationship'), max_length=50, blank=True, null=True)
    next_of_kin_phone_number = models.CharField(_('Phone Number'), max_length=20, blank=True, null=True)
    next_of_kin_address = models.CharField(_('Address'), max_length=500, blank=True, null=True)

    # SPIRITUAL INFORMATION
    gift_graces = models.CharField(_("Gift & Graces"), max_length=500, blank=True, null=True)
    callings = models.CharField(_("Callings"), max_length=500, blank=True, null=True)
    reveal_calling_by_shepherd = models.BooleanField(_("Reveal Calling to Sheep"), default=False)

    # ADDITIONAL INFORMATION
    unit_of_work = models.CharField(_("Unit of Work"), max_length=200, blank=True, null=True)
    shepherd = models.ForeignKey('Shepherd', on_delete=models.SET_NULL, blank=True, null=True)
    sub_shepherd = models.ForeignKey('SubShepherd', on_delete=models.SET_NULL, blank=True, null=True)

    last_active_date = models.DateField(_("Last active date"), default=timezone.now)

    # SPECIAL KNOWLEDGE
    shoe_size = models.CharField(_("Shoe Size"), max_length=20, blank=True, null=True)
    cloth_size = models.CharField(_("Cloth Size"), max_length=20, blank=True, null=True)
    level = models.CharField(_('Level'), max_length=15, default='new_mem', choices=LEVEL_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.first_name} {self.last_name} @{self.username}"

    class Meta:
        ordering = ('first_name', )
        verbose_name = "User"
        verbose_name_plural = "Users"

    @admin.display(ordering='date_of_birth', description="Age")
    def get_user_age(self):
        if self.date_of_birth:
            now = datetime.datetime.now()
            current_age = now.year - self.date_of_birth.year

            return current_age
        return None

    def set_date_of_birth(self, dob):
        dob = Validators.validate_prevent_future_date(value=dob)

        self.date_of_birth = dob

    def get_iso_date_of_birth(self):
        return self.date_of_birth.isoformat()

    def __validate_leader_roles__(self, leader, role=None):
        if role is None:
            print("I will assume leader is a shepherd")
        user_full_name = self.__str__()

        if role is None:
            leader_full_name = leader.get_shepherd_full_name()
        else:
            leader_full_name = leader.get_subshepherd_full_name()

        if user_full_name == leader_full_name:
            raise ValidationError(f"User can't be a {'Shepherd' if role is None else 'Sub Shepherd'} to himself")

    def set_shepherd(self, shepherd):
        self.__validate_leader_roles__(shepherd)
        self.shepherd = shepherd

    def set_subshepherd(self, sub_shepherd):
        self.__validate_leader_roles__(sub_shepherd, 'sub')
        self.sub_shepherd = sub_shepherd

    def to_dict(self):
        data = {
            'first_name': self.first_name,
            'surname': self.last_name,
            'gender': self.gender,
            'date_of_birth': self.date_of_birth.isoformat(),
            'phone_number': self.phone_number,
            'about': self.about,
            'email': self.email,
            'occupation': self.occupation,
            'address': self.address,
            'skills': self.skills,
            'blood_group': self.blood_group,
            'genotype': self.genotype,
            'chronic_illness': self.chronic_illness,

            'lga': self.lga, 'state': self.state, 'country': self.country,

            'course_of_study': self.course_of_study,
            'years_of_study': self.years_of_study,
            'current_year_of_study': self.current_year_of_study,
            'final_year_status': self.final_year_status,

            'next_of_kin_full_name': self.next_of_kin_full_name,
            'next_of_kin_relationship': self.next_of_kin_relationship,
            'next_of_kin_phone_number': self.next_of_kin_phone_number,
            'next_of_kin_address': self.next_of_kin_address,

            'gift_graces': self.gift_graces, 'unit_of_work': self.unit_of_work,
            'shepherd': self.shepherd if self.shepherd else "",
            'sub_shepherd': self.sub_shepherd if self.shepherd else "",

            'shoe_size': self.shoe_size, 'cloth_size': self.cloth_size,
        }
        return data


class Permission(models.Model):
    name = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, to_field='username')
    can_edit_catalog = models.BooleanField(default=False)
    head_of_department = models.BooleanField(default=False)

    def __str__(self):
        return str(self.name)


class FamilyMemberWeeklySchedule(models.Model):
    username = models.OneToOneField(get_user_model(), on_delete=models.CASCADE, to_field='username', primary_key=True)

    def __str__(self):
        return f"Weekly Schedule for: {str(self.username)}"


OUT_CHOICES = (
    (None, 'None'),
    ('annex', 'Annex/Street'),
    ('permsite', 'Permsite/Street'),
    ('work_online', 'Work/Online Evangelism')
)


# Create your models here.
class WeekOne(models.Model):
    family_schedule = models.OneToOneField(FamilyMemberWeeklySchedule, on_delete=models.CASCADE, to_field='username')
    In = models.BooleanField(default=False)
    out = models.CharField(max_length=25, choices=OUT_CHOICES, null=True, blank=True)
    wednesday = models.BooleanField(default=False)
    exception = models.BooleanField(default=False)

    def __str__(self):
        return f"Week One"

    class Meta:
        verbose_name_plural = 'Week One'


class WeekTwo(models.Model):
    family_schedule = models.OneToOneField(FamilyMemberWeeklySchedule, on_delete=models.CASCADE, to_field='username')
    In = models.BooleanField(default=False)
    out = models.CharField(max_length=25, choices=OUT_CHOICES, null=True, blank=True)
    wednesday = models.BooleanField(default=False)
    exception = models.BooleanField(default=False)

    def __str__(self):
        return f"Week Two"

    class Meta:
        verbose_name_plural = 'Week Two'


class WeekThree(models.Model):
    family_schedule = models.OneToOneField(FamilyMemberWeeklySchedule, on_delete=models.CASCADE, to_field='username')
    In = models.BooleanField(default=False)
    out = models.CharField(max_length=25, choices=OUT_CHOICES, null=True, blank=True)
    wednesday = models.BooleanField(default=False)
    exception = models.BooleanField(default=False)

    def __str__(self):
        return f"Week Three"

    class Meta:
        verbose_name_plural = 'Week Three'


class WeekFour(models.Model):
    family_schedule = models.OneToOneField(FamilyMemberWeeklySchedule, on_delete=models.CASCADE, to_field='username')
    In = models.BooleanField(default=False)
    out = models.CharField(max_length=25, choices=OUT_CHOICES, null=True, blank=True)
    wednesday = models.BooleanField(default=False)
    exception = models.BooleanField(default=False)

    def __str__(self):
        return f"Week Four"

    class Meta:
        verbose_name_plural = 'Week Four'
