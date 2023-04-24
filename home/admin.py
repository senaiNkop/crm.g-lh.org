from django.contrib import admin
from .models import RecentActivity


@admin.register(RecentActivity)
class RecentActivity(admin.ModelAdmin):
    list_display = ('username', 'date', 'category')
    list_filter = ('username', 'category')

    # FIXME: ADD FUNCTIONALITY TO DELETE THE OLDEST ROW IF IT EXCEEDS 10 ENTRIES
    # FIXME: FOR A PARTICULAR USER.
