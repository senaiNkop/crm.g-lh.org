
from django.urls import path
from .views import (PropheticVisionListView, UpdatePropheticVisionListView,
                    PropheticVisionDetailView, UpdatePropheticVisionDetailView)

app_name = 'prophetic_vision'
urlpatterns = [
    path('', PropheticVisionListView.as_view(), name='list'),
    path('<str:name>/<str:month>/<str:year>/<int:pk>/', PropheticVisionDetailView.as_view(), name='detail'),
    path('update/list/', UpdatePropheticVisionListView.as_view(), name='update-list'),
    path('update/detail/<int:pk>/', UpdatePropheticVisionDetailView.as_view(), name='update-detail'),
]
