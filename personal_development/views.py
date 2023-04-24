
from datetime import datetime, time

from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import get_user_model

from .models import BibleReading, PrayerMarathon
from home.models import RecentActivity

# Create your views here.

title = 'GLH-FAM'


class BibleReadingListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('users-login')
    template_name = 'dashboard/table/table-data.html'
    context_object_name = 'lists'

    def get_queryset(self):
        username = get_object_or_404(get_user_model(), username=self.request.user.username)
        return BibleReading.objects.filter(username=username).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['bible_challenge_on'] = True
        context['category'] = 'Bible Reading'
        context['user'] = self.request.user
        context['title'] = title

        return context


class UpdateBibleReadingListView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('users-login')
    template_name = "dashboard/table/table-data.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['bible_challenge_on'] = True
        context['category'] = 'Bible Reading'
        context['user'] = self.request.user
        context['title'] = title

        return context

    def post(self, request, **kwargs):

        try:
            bible_passage = request.POST['bible_passage']
        except:
            bible_passage = request.POST['custom_bible_passage']

        comment = request.POST['bible_reading_comment']
        date = request.POST['bible_reading_date']
        status = request.POST['bible_reading_status']

        bible_reading = BibleReading(bible_passage=bible_passage, comment=comment,
                                     date=datetime.strptime(date, '%m/%d/%Y'), status=status,
                                     username=request.user)
        bible_reading.save()

        recent = RecentActivity(username=request.user, category="bible_reading",
                                details=f"Read {bible_passage}")
        recent.save()

        return HttpResponseRedirect(reverse_lazy('bible_reading:list'))


class BibleReadingDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('users-login')
    template_name = 'dashboard/special-pages/detail.html'
    context_object_name = 'detail'
    model = BibleReading

    def get_context_data(self, **kwargs):
        context = super(BibleReadingDetailView, self).get_context_data(**kwargs)

        context['category'] = 'Bible Reading'
        context['user'] = self.request.user
        context['title'] = title

        return context


class UpdateBibleReadingDetailView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('bible-reading-detail')
    template_name = 'dashboard/special-pages/detail.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateBibleReadingDetailView, self).get_context_data(**kwargs)

        context['category'] = 'Bible Reading'
        context['user'] = self.request.user
        context['title'] = title

        return context

    def post(self, request, **kwargs):

        comment = request.POST['comment']
        date = request.POST['date']
        status = request.POST['status']

        bible_reading = BibleReading.objects.get(id=kwargs['pk'], bible_passage=kwargs['passage'], username=request.user)

        bible_reading.comment = comment
        bible_reading.status = status
        bible_reading.date = datetime.strptime(date, '%m/%d/%Y')

        bible_reading.save()

        recent = RecentActivity(username=request.user, category="bible_reading",
                                details=f"Updated {kwargs['passage']}")
        recent.save()
        return JsonResponse({'love': 'you'})


class PrayerMarathonListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('users-login')
    template_name = 'dashboard/table/table-data.html'
    context_object_name = 'lists'

    def get_queryset(self):
        username = get_object_or_404(get_user_model(), username=self.request.user.username)
        return PrayerMarathon.objects.filter(username=username).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['category'] = 'Prayer Marathon'
        context['user'] = self.request.user
        context['title'] = title

        return context


class UpdatePrayerMarathonListView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('users-login')
    template_name = "dashboard/table/table-data.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['category'] = 'Prayer Marathon'
        context['user'] = self.request.user
        context['title'] = title

        return context

    def post(self, request, **kwargs):

        comment = request.POST['prayer_marathon_comment']
        date = request.POST['prayer_marathon_date']

        prayer_marathon = PrayerMarathon(comment=comment,
                                         date=datetime.strptime(date, '%m/%d/%Y'),
                                         username=request.user)

        prayer_marathon.save()

        recent = RecentActivity(username=request.user, category="prayer_marathon",
                                details='Intercession')
        recent.save()

        return HttpResponseRedirect(reverse_lazy('prayer_marathon:list'))


class PrayerMarathonDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('users-login')
    template_name = 'dashboard/special-pages/detail.html'
    context_object_name = 'detail'
    model = PrayerMarathon

    def get_context_data(self, **kwargs):
        context = super(PrayerMarathonDetailView, self).get_context_data(**kwargs)

        context['category'] = 'Prayer Marathon'
        context['user'] = self.request.user
        context['title'] = title

        return context


class UpdatePrayerMarathonDetailView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('users-login')
    template_name = 'dashboard/special-pages/detail.html'

    def get_context_data(self, **kwargs):
        context = super(UpdatePrayerMarathonDetailView, self).get_context_data(**kwargs)

        context['category'] = 'Prayer Marathon'
        context['user'] = self.request.user
        context['title'] = title

        return context

    def post(self, request, **kwargs):
        comment = request.POST['comment']
        date = request.POST['date']

        prayer_marathon = PrayerMarathon.objects.get(id=kwargs['pk'], username=request.user)
        prayer_marathon.comment = comment
        prayer_marathon.date = datetime.strptime(date, '%m/%d/%Y')

        prayer_marathon.save()

        # Save Recent Activity
        recent = RecentActivity(username=request.user, category="prayer_marathon",
                                details='Intercession')
        recent.save()
        return JsonResponse({'love': 'you'})
