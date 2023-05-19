from django.urls import path

from .views import DashboardView, SheepSummaryDetailView

app_name = 'pastoring'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('<str:shepherd>/sheep/<str:sheep>/details', SheepSummaryDetailView.as_view(), name='sheep-summary'),

    # path('church-work/', )
]