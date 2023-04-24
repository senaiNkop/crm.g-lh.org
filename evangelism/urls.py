
from django.urls import path

from .views import (EvangelismListView, UpdateEvangelismListView,
                    EvangelismDetailView, UpdateEvangelismDetailView)

app_name = 'evangelism'
urlpatterns = [
    path('', EvangelismListView.as_view(), name='list'),
    path('<int:pk>/', EvangelismDetailView.as_view(), name='detail'),
    path('update/list/', UpdateEvangelismListView.as_view(), name='update-list'),
    path('update/detail/<int:pk>/', UpdateEvangelismDetailView.as_view(), name='update-detail')
]

