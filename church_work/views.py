
from datetime import datetime, time

from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy, resolve
from django.http import HttpResponseRedirect, JsonResponse
from django.contrib.auth import get_user_model

from .models import ChurchWork
from home.models import RecentActivity

title = 'GLH-FAM'


class ChurchWorkListView(LoginRequiredMixin, ListView):
    login_url = reverse_lazy('users-login')
    template_name = 'dashboard/table/table-data.html'
    context_object_name = 'lists'

    def get_queryset(self):
        username = get_object_or_404(get_user_model(), username=self.request.user.username)
        return ChurchWork.objects.filter(username=username).order_by('-date')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['category'] = 'Church Work'
        context['user'] = self.request.user
        context['title'] = title

        return context


class UpdateChurchWorkListView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('users-login')
    template_name = "dashboard/table/table-data.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['category'] = 'Church Work'
        context['user'] = self.request.user
        context['title'] = title

        return context

    def post(self, request, **kwargs):
        details = request.POST['church_work_details']
        work_category = request.POST['church_work_category']
        hours_spent = request.POST['church_work_hours_spent']
        start_time = request.POST['church_work_start_time']
        end_time = request.POST['church_work_end_time']
        date = request.POST['church_work_date']

        church_work = ChurchWork(details=details, work_category=work_category,
                                 hours_spent=int(hours_spent), start_time=start_time,
                                 end_time=end_time, date=datetime.strptime(date, '%m/%d/%Y'),
                                 username=request.user)
        church_work.save()

        recent = RecentActivity(username=request.user, category="church_work",
                                details=f"Worked on {work_category}")
        recent.save()

        return HttpResponseRedirect(reverse_lazy('church_work:list'))


class ChurchWorkDetailView(LoginRequiredMixin, DetailView):
    login_url = reverse_lazy('users-login')
    template_name = 'dashboard/special-pages/detail.html'
    context_object_name = 'detail'
    model = ChurchWork

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['category'] = 'Church Work'
        context['user'] = self.request.user
        context['title'] = title

        return context


class UpdateChurchWorkDetailView(LoginRequiredMixin, TemplateView):
    login_url = reverse_lazy('users-login')
    template_name = 'dashboard/special-pages/detail.html'

    def get_context_data(self, **kwargs):
        context = super(UpdateChurchWorkDetailView, self).get_context_data(**kwargs)

        context['category'] = 'Church Work'
        context['user'] = self.request.user
        context['title'] = title

        return context

    def post(self, request, **kwargs):
        details = request.POST['details']
        work_category = request.POST['work_category']
        hours_spent = request.POST['hours_spent']
        start_time = request.POST['start_time']
        end_time = request.POST['end_time']
        date = request.POST['date']

        church_work = ChurchWork.objects.get(id=kwargs['pk'])
        church_work.details = details
        church_work.work_category = work_category
        church_work.start_time = time.fromisoformat(start_time)
        church_work.end_time = time.fromisoformat(end_time)
        church_work.hours_spent = hours_spent
        church_work.date = datetime.strptime(date, '%m/%d/%Y')

        church_work.save()

        recent = RecentActivity(username=request.user, category="church_work",
                                details=f'Worked on {work_category}')
        recent.save()

        return JsonResponse({'love': 'You'})
