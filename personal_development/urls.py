from django.urls import path, include

from .views import (
    BibleReadingListView, BibleReadingDetailView, UpdateBibleReadingDetailView, UpdateBibleReadingListView,
    PrayerMarathonListView, PrayerMarathonDetailView, UpdatePrayerMarathonDetailView, UpdatePrayerMarathonListView,
)

bible_reading = [
    path('', BibleReadingListView.as_view(), name='list'),
    path('<str:passage>/<int:pk>/', BibleReadingDetailView.as_view(), name='detail'),
    path('update/detail/<int:pk>/<str:passage>/', UpdateBibleReadingDetailView.as_view(), name='update-detail'),
    path('update/list/', UpdateBibleReadingListView.as_view(), name='update-list'),
]

prayer_marathon = [
    path('', PrayerMarathonListView.as_view(), name='list'),
    path('<int:pk>/', PrayerMarathonDetailView.as_view(), name='detail'),
    path('update/detail/<int:pk>/', UpdatePrayerMarathonDetailView.as_view(), name='update-detail'),
    path('update/list/', UpdatePrayerMarathonListView.as_view(), name='update-list')
]


urlpatterns = [
    path('bible-reading/', include((bible_reading, 'personal_development'), namespace='bible_reading')),
    path('prayer-marathon/', include((prayer_marathon, 'personal_development'), namespace='prayer_marathon')),
]
