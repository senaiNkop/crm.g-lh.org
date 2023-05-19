
from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from . import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet, basename='customuser')
router.register(r'shepherds', views.ShepherdViewSet, basename='shepherd')
router.register(r'sub-shepherds', views.SubShepherdViewSet, basename='subshepherd')
router.register(r'permissions', views.PermissionViewSet, basename='permission')
router.register(r'catalogs', views.CatalogViewSet, basename='catalog')
router.register(r'family-schedule', views.FamilyWeeklyScheduleViewSet, basename='familymemberweeklyschedule')
router.register(r'week-one', views.WeekOneViewSet, basename='weekone')
router.register(r'week-two', views.WeekTwoViewSet, basename='weektwo')
router.register(r'week-three', views.WeekThreeViewSet, basename='weekthree')
router.register(r'week-four', views.WeekFourViewSet, basename='weekfour')
# router.register(r'weekone', views.WeekFour.)

urlpatterns = [
    path('', include(router.urls)),
    path('api-token-auth', obtain_auth_token)
]