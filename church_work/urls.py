
from django.urls import path, include


from .views import (ChurchWorkListView, UpdateChurchWorkListView,
                    ChurchWorkDetailView, UpdateChurchWorkDetailView)

app_name = 'church_work'
urlpatterns = [
    path('', ChurchWorkListView.as_view(), name='list'),
    path('<int:pk>/', ChurchWorkDetailView.as_view(), name='detail'),
    path('update/list/', UpdateChurchWorkListView.as_view(), name='update-list'),
    path('update/detail/<int:pk>/', UpdateChurchWorkDetailView.as_view(), name='update-detail'),
]
