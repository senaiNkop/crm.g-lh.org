import pandas as pd
import numpy as np

from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse

from django.views.generic.base import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model

from django.core.exceptions import ValidationError

from users.models import FamilyMemberWeeklySchedule
from .models import RecentActivity

from personal_development.models import BibleReading, PrayerMarathon
from church_work.models import ChurchWork
from evangelism.models import Evangelism

from users.models import Catalog, Shepherd, SubShepherd, CustomUser, Permission
from users.my_models.users import GENOTYPE_CHOICES, BLOOD_GROUP_CHOICES

developers = "God's Lighthouse Developers Team (GDevT)"
title = 'GLH-FAM'

days = {
    'Mon': 0, 'Tue': 1, 'Wed': 2, 'Thu': 3, 'Fri': 4, 'Sat': 5, 'Sun': 6
}

months = {
    'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'Jun': 5,
    'Jul': 6, 'Aug': 7, 'Sept': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11
}


def sort_function(series):
    val = series[0]
    if val in days.keys():
        rule = days
    elif val in months.keys():
        rule = months

    return series.apply(lambda x: rule[x])


# Create your views here.
class Home(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('users-login')
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super(Home, self).get_context_data(**kwargs)
        recent = RecentActivity.custom_objects.auto_delete_old_activities(username=self.request.user)

        context['category'] = 'Homepage'
        context['developers'] = developers
        context['user'] = self.request.user
        context['title'] = title
        context['recent_activity'] = recent

        try:
            member_schedule = FamilyMemberWeeklySchedule.objects.get(username=self.request.user)
        except FamilyMemberWeeklySchedule.DoesNotExist:
            context['member_schedule'] = False
        else:
            context['member_schedule'] = True

            week_one = member_schedule.weekone
            week_two = member_schedule.weektwo
            week_three = member_schedule.weekthree
            week_four = member_schedule.weekfour

            context['week_one'] = week_one
            context['week_two'] = week_two
            context['week_three'] = week_three
            context['week_four'] = week_four

        return context


class Profile(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('users-login')
    template_name = 'dashboard/app/user-profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['category'] = 'Profile'
        context['developers'] = developers
        context['user'] = self.request.user
        context['title'] = title

        context['shepherd'] = Shepherd.objects.all().exclude(name=self.request.user)
        context['sub_shepherd'] = SubShepherd.objects.all().exclude(name=self.request.user)

        context['genotype'] = GENOTYPE_CHOICES
        context['blood_group'] = BLOOD_GROUP_CHOICES

        return context

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)
        form = request.POST['form_name']

        if form.lower().strip() == 'password':
            current_password = request.POST['current']
            new_password = request.POST['new']
            # get user using password as a means of confirmation

            user = request.user

            if not user.check_password(current_password):
                return JsonResponse({'confirm': False}, safe=False)

            user.set_password(new_password)
            user.save()

            recent = RecentActivity(username=request.user, category="bio_data",
                                    details='Changed Password')
            recent.save()
            return JsonResponse({'confirm': True}, safe=False)

        elif form.lower().strip() == 'profile':

            user: CustomUser = request.user

            # BIO DATA

            user.first_name = request.POST['first_name']
            user.last_name = request.POST['surname']
            user.gender = request.POST['gender']

            # validate and set the date of birth
            try:
                user.set_date_of_birth(request.POST['date_of_birth'])
            except ValidationError:
                return JsonResponse({'error': "Your birth date should not be now or in the future"})

            user.about = request.POST['about']

            # PERSONAL DATA
            user.phone_number = request.POST['phone_number']
            user.email = request.POST['email']
            user.occupation = request.POST['occupation']
            user.address = request.POST['address']
            user.skills = request.POST['skills']

            # BASIC MEDICAL INFORMATION
            user.blood_group = request.POST['blood_group']
            user.genotype = request.POST['genotype']
            user.chronic_illness = request.POST['chronic_illness']

            # RESIDENTIAL INFORMATION
            user.lga = request.POST['lga']
            user.state = request.POST['state']
            user.country = request.POST['country']

            # SCHOOL INFORMATION
            user.course_of_study = request.POST['course_of_study']
            user.years_of_study = request.POST['years_of_study']
            user.current_year_of_study = request.POST['current_year_of_study']
            user.final_year_status = request.POST['final_year_status']

            # NEXT OF KIN INFORMATION
            user.next_of_kin_full_name = request.POST['next_of_kin_full_name']
            user.next_of_kin_relationship = request.POST['next_of_kin_relationship']
            user.next_of_kin_phone_number = request.POST['next_of_kin_phone_number']
            user.next_of_kin_address = request.POST['next_of_kin_address']

            # SPIRITUAL INFORMATION
            user.gift_graces = request.POST['gift_graces']

            # ADDITIONAL INFORMATION
            user.unit_of_work = request.POST['unit_of_work']

            shepherd = request.POST['shepherd'].strip()
            if shepherd:
                shepherd = get_user_model().objects.get(username=request.POST['shepherd'])
                shepherd = Shepherd.objects.get(name=shepherd)
                user.shepherd = shepherd
            else:
                user.shepherd = None

            sub_shepherd = request.POST['sub_shepherd'].strip()
            if sub_shepherd:
                sub_shepherd = get_user_model().objects.get(username=request.POST['sub_shepherd'])
                sub_shepherd = SubShepherd.objects.get(name=sub_shepherd)
                user.sub_shepherd = sub_shepherd
            else:
                user.sub_shepherd = None

            # SPECIAL KNOWLEDGE
            user.shoe_size = request.POST['shoe_size']
            user.cloth_size = request.POST['cloth_size']

            try:
                user.profile_pic = request.FILES['profile_pic']
            except Exception as e:
                pass

            user.save()

            recent = RecentActivity(username=request.user, category="bio_data",
                                    details='Updated Bio Data')
            recent.save()

            return JsonResponse({'confirm': True}, safe=False)


class CatalogView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('users_login')
    template_name = 'dashboard/table/catalog_table.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['category'] = 'Catalog'
        context['developers'] = developers
        context['user'] = self.request.user
        context['title'] = title

        return context

    def get(self, request, *args, **kwargs):
        if 'unique_id' in request.GET:
            unique_id = request.GET['unique_id']

            try:
                catalog = Catalog.objects.get(id=unique_id)
            except Catalog.DoesNotExist:
                return JsonResponse({'confirm': False})
            else:

                return JsonResponse({'confirm': True, 'catalog': catalog.get_cleaned_fields_in_dict()})
        else:
            return super().get(request, *args, **kwargs)

    def post(self, request, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = 'Catalog'
        context['developers'] = developers
        context['user'] = self.request.user
        context['title'] = title

        search_text = request.POST['search_text']

        results = Catalog.objects.filter(things_spoken_about__icontains=search_text)
        context['results'] = results
        context['no_of_results'] = len(results)
        context['search_text'] = search_text

        return self.render_to_response(context)


class Registration(TemplateView):
    template_name = 'dashboard/auth/sign-up.html'

    def get_context_data(self, **kwargs):
        context = super(Registration, self).get_context_data(**kwargs)
        context['developers'] = developers
        context['title'] = title

        return context

    def post(self, request, **kwargs):
        context = self.get_context_data(**kwargs)

        first_name = request.POST['first_name']
        surname = request.POST['last_name']
        username = request.POST['username']
        gender = request.POST['gender']
        password = request.POST['password']

        email = request.POST['email']
        phone_number = request.POST['phone_number']
        address = request.POST['address']
        occupation = request.POST['occupation']

        user = get_user_model().objects.create_user(email=email, password=password, save=False,
                                                     first_name=first_name, last_name=surname,
                                                     username=username, gender=gender, phone_number=phone_number,
                                                     address=address, occupation=occupation)

        try:
            user.save()
        except BaseException as e:
            error = str(e)
            if 'email' in error:
                context['error'] = "This email already have an account"
            else:
                context['error'] = f"This username '{username}' is already taken"
            return self.render_to_response(context)

        # Save the this specific user's permission
        permissions = Permission(name=user, is_shepherd=False, is_subshepherd=False,
                                 can_edit_catalog=False, head_of_department=False)

        permissions.save()

        login(request, user)
        return HttpResponseRedirect(reverse_lazy('home'))


def logout_user(request):
    logout(request)
    return HttpResponseRedirect(reverse_lazy('users-login'))


class Login(TemplateView):
    template_name = 'dashboard/auth/sign-in.html'

    def get_context_data(self, **kwargs):
        context = super(Login, self).get_context_data()
        context['developers'] = developers
        context['title'] = title

        return context

    def post(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)

        email_username = request.POST['email_username']
        password = request.POST['password']

        user = authenticate(request, email=email_username, password=password)

        if user is None:
            # Username is used for login

            User = get_user_model()

            try:
                user = User.objects.get(username=email_username)
            except User.DoesNotExist:
                context['error'] = True
                return self.render_to_response(context)

            confirm_password = user.check_password(password)

            if not confirm_password:
                context['error'] = True
                return self.render_to_response(context)

        login(request, user)
        return HttpResponseRedirect(reverse_lazy('home'))


# @@@@@@@############@############################################

# UPDATE DASHBOARD COUNTER

# ##########################@@@@@@@@@@@@@@@@@@@@@@@@


class CounterUpdate(LoginRequiredMixin, TemplateView):
    """
    Return the total number of passages or prayers that has been read by
    the user
    """
    login_url = reverse_lazy('users-login')

    def get(self, request, **kwargs):
        print(f'\n\n\n{request}\n\n\n')

        bible_reading = BibleReading.objects.filter(username=request.user)
        prayer_marathon = PrayerMarathon.objects.filter(username=request.user)
        church_work = ChurchWork.objects.filter(username=request.user)
        evangelism = Evangelism.objects.filter(username=request.user)

        context = {
            'counter_passages': bible_reading.count(),
            'counter_prayers': prayer_marathon.count(),
            'counter_church_works': church_work.count(),
            'counter_evangelism': evangelism.count()
        }

        return JsonResponse(context)


class ChartBibleReading(LoginRequiredMixin, TemplateView):
    """
    Return the total number of passages or prayers that has been read by
    the user
    """
    login_url = reverse_lazy('users-login')

    def get(self, request, **kwargs):
        print(f'\n\n\n{request}\n\n\n')

        category = kwargs['category']
        mode = kwargs['mode']

        context = {
            'category': category,
            'mode': mode
        }
        if category == 'All':
            bible_reading_dates = BibleReading.data_analysis.date_series(request.user)
            prayer_marathon_dates = PrayerMarathon.data_analysis.date_series(request.user)

            return JsonResponse(context)

        elif category == 'Bible Reading':
            dates = BibleReading.data_analysis.date_series(request.user)

        elif category == 'Prayer Marathon':
            dates = PrayerMarathon.data_analysis.date_series(request.user)

        elif category == 'Church Work':
            dates = ChurchWork.data_analysis.date_series(request.user)

        elif category == 'Evangelism':
            fields = [
                'no_of_people_prayed', 'no_led_to_christ',
                'follow_up', 'holy_spirit_baptism'
            ]
            motivator = Evangelism.objects.filter(username=request.user).values_list('no_of_people_prayed',
                                                                                     'no_led_to_christ',
                                                                                     'follow_up', 'holy_spirit_baptism')
            denominator = 1000
            percent = 100

            people_prayed = int(sum(motivator.values_list('no_of_people_prayed', flat=True)))
            led_to_christ = int(sum(motivator.values_list('no_led_to_christ', flat=True)))
            follow_up = int(sum(motivator.values_list('follow_up', flat=True)))
            baptism = int(sum(motivator.values_list('holy_spirit_baptism', flat=True)))

            people_prayed_percentage = (people_prayed / denominator) * percent
            led_to_christ_percentage = (led_to_christ / denominator) * percent
            follow_up_percentage = (follow_up / denominator) * percent
            baptism_percentage = (baptism / denominator) * percent

            raw = [people_prayed, led_to_christ, follow_up, baptism]
            values = [people_prayed_percentage, led_to_christ_percentage,
                      follow_up_percentage, baptism_percentage]

            context['distinct_values'] = fields
            context['unique_counts'] = values
            context['raw_values'] = raw

            return JsonResponse(context)

        else:
            # pass
            assert False, "You are not suppose to be here"

        if dates.empty:
            if mode == 'daily':
                context['distinct_values'] = list(days.keys())
                context['unique_counts'] = [0] * len(days.keys())
            elif mode == 'monthly':
                context['distinct_values'] = list(months.keys())
                context['unique_counts'] = [0] * len(months.keys())
            elif mode == 'monthly':
                context['distinct_values'] = [' ', ' ']
                context['unique_counts'] = [0, 0]

            return JsonResponse(context)

        if mode == 'daily':
            dates = dates.strftime('%a')
        elif mode == 'monthly':
            dates = dates.strftime('%b')
        elif mode == 'yearly':
            dates = dates.strftime('%Y')

        distinct_values, unique_counts = np.unique(dates, return_counts=True)

        data = {
            'distinct_values': distinct_values,
            'unique_counts': unique_counts
        }

        df = pd.DataFrame(data)

        if mode == 'daily':
            df = df.sort_values(by='distinct_values', key=sort_function)
        elif mode == 'monthly':
            df = df.sort_values(by='distinct_values', key=sort_function)
        elif mode == 'yearly':
            df = df.sort_values(by='distinct_values')

        context['distinct_values'] = list(df['distinct_values'])
        context['unique_counts'] = [int(x) for x in df['unique_counts']]

        return JsonResponse(context, safe=False)
