import os
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _


def get_user_name(object, fname):
    _, ext = os.path.splitext(fname)
    username = object.username
    return f"profile_pics/{username}{ext}"


class Validators(object):
    @staticmethod
    def validate_prevent_future_date(value):
        """
        Ensure that the age of the user is not younger than two years
        or in the future
        """
        now = datetime.date.today()

        if isinstance(value, str):
            value = datetime.date.fromisoformat(value)
        if value > now:
            raise ValidationError(_("Your birth date %(dob)s should not be in the future"),
                                  params={'dob': value})
        return value

    @staticmethod
    def validate_shepherding_structure(value, obj):
        """
        Ensure that the shepherd are not shepherd and sub shepherd of themself
        """

        username = obj.username

        if username == value:
            raise ValidationError(_("You can't be shepherd of yourself"))


    @staticmethod
    def validate_sub_shepherd_structure(value, obj):
        """
        Ensure that the subsherd are not shepherd of them
        """







