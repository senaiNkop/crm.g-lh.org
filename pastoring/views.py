from django.urls import reverse_lazy
from django.http import HttpResponseRedirect, HttpResponseForbidden

from django.views.generic.base import TemplateView

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import get_user_model

from users.models import Shepherd, SubShepherd, CustomUser
from church_work.models import ChurchWork

developers = "God's Lighthouse Developers Team (GDevT)"
title = 'GLH-FAM'


# Create your views here.
class DashboardView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('users-login')
    template_name = 'pastoring/index.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_staff and (
                self.request.user.level == 'sub_shep' or self.request.user.level == 'core_shep' or self.request.user.level == 'chief_shep'):
            return super().get(request, *args, **kwargs)
        return HttpResponseForbidden("You are not a Shepherd...please go back")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['category'] = 'Dashboard'
        context['developers'] = developers
        context['user'] = self.request.user
        context['title'] = title

        # TODO: Sort by sheep activeness
        user = self.request.user

        if user.level == 'core_shep' or user.level == 'chief_shep':
            shepherd = Shepherd.objects.get(name=user)
        elif user.level == 'sub_shep':
            shepherd = SubShepherd.objects.get(name=user)
        else:
            # if by mistake someone slips through
            return HttpResponseForbidden("How do you get here!")

        context['shepherd'] = shepherd

        if user.level == 'chief_shep':
            context['core_shepherd'] = Shepherd.objects.all().exclude(name=user)

        elif user.level == 'core_shep':

            context['sheep'] = get_user_model().objects.get_shepherd_sheep(shepherd=shepherd)

        elif user.level == 'sub_shep':
            context['sheep'] = get_user_model().objects.get_sub_shepherd_sheep(sub_shepherd=shepherd)

        return context


class ShepherdSheepListView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('users-login')
    template_name = 'pastoring/shepherd_sheep_list.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_staff and (self.request.user.level == 'chief_shep'):
            return super().get(request, *args, **kwargs)
        return HttpResponseForbidden("You are not a Shepherd...please go back")

    def get_context_data(self, **kwargs):
        context = super().get_context_data()

        context['category'] = 'Shepherd List'
        context['developers'] = developers

        shepherd = Shepherd.objects.get(id=kwargs['pk'])
        sheep = get_user_model().objects.get_shepherd_sheep(shepherd)

        context['shepherd'] = shepherd
        context['sheep'] = sheep

        return context



class SheepSummaryDetailView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('users-login')
    template_name = 'pastoring/sheep_summary_details.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_staff and (self.request.user.level == 'sub_shep' or self.request.user.level == 'core_shep'
                                           or self.request.user.level == 'chief_shep'):
            return super().get(request, *args, **kwargs)
        return HttpResponseForbidden("You are not a Shepherd...please go back")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['category'] = 'Dashboard'
        context['developers'] = developers
        context['user'] = self.request.user
        context['title'] = title

        sheep: CustomUser = get_user_model().objects.get(username=kwargs['sheep'])

        context['sheep'] = sheep
        context['church_work'] = sheep.churchwork_set.all().order_by('-date')

        return context


class ChurchWorkView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('users-login')
    template_name = 'pastoring/sheep_summary_details.html'

    def get(self, request, *args, **kwargs):
        if self.request.user.is_staff and (
                self.request.user.level == 'sub_shep' or self.request.user.level == 'core_shep'
                or self.request.user.level == 'chief_shep'):
            return super().get(request, *args, **kwargs)
        return HttpResponseForbidden("You are not a Shepherd...please go back")
