from django.urls import path, include
from .views import (Home, Profile, Registration, Login, logout_user, CounterUpdate,
                    ChartBibleReading, CatalogView, TaskView)


urlpatterns = [
    path('', Home.as_view(), name='home'),
    path('<str:username>/users-profile/', Profile.as_view(), name='users-profiles'),
    path('users-registration/', Registration.as_view(), name='users-registration'),
    path('users-login/', Login.as_view(), name='users-login'),
    path('users-logout/', logout_user, name='users-logout'),
    path('users-tasks/', TaskView.as_view(), name='users-task'),

    path('personal-development/', include('personal_development.urls')),
    path('church-work/', include('church_work.urls')),
    path('evangelism/', include('evangelism.urls')),
    path('prophetic-vision/', include('prophetic_vision.urls')),

    path('catalog/', CatalogView.as_view(), name='catalog'),
    path('update-counter/', CounterUpdate.as_view(), name='update-counter'),
    path('update-counter/<str:category>/<str:mode>/', ChartBibleReading.as_view(), name='update-charts'),

    path('hod-report/', include('hod_report.urls')),
    path('pastoring/', include('pastoring.urls')),
]
