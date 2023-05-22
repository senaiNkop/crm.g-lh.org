from django.urls import path, include

from .views import (
    BibleReadingListView, BibleReadingDetailView,
    PrayerMarathonListView, PrayerMarathonDetailView
)

bible_reading = [
    path('', BibleReadingListView.as_view(), name='list'),
    path('<str:passage>/<int:pk>/', BibleReadingDetailView.as_view(), name='detail'),
]

prayer_marathon = [
    path('', PrayerMarathonListView.as_view(), name='list'),
    path('<int:pk>/', PrayerMarathonDetailView.as_view(), name='detail'),
]


urlpatterns = [
    path('bible-reading/', include((bible_reading, 'personal_development'), namespace='bible_reading')),
    path('prayer-marathon/', include((prayer_marathon, 'personal_development'), namespace='prayer_marathon')),
]
