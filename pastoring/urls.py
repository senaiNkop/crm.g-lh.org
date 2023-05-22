from django.urls import path
from .views import (DashboardView, SheepSummaryDetailView, ShepherdSheepListView)


app_name = 'pastoring'
urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),
    path('chief-shepherd/shepherd/<int:pk>/', ShepherdSheepListView.as_view(), name='shepherd-list'),
    path('<str:shepherd>/sheep-info/<str:sheep>/', SheepSummaryDetailView.as_view(), name='sheep-summary'),
]