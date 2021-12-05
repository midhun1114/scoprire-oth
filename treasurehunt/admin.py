from csvexport.actions import csvexport
from django.contrib import admin
from django.contrib.admin.models import LogEntry
from django.contrib.auth.models import User

from treasurehunt.models import Score, AnswerChecker, level, userProfile

# Register your models here.
admin.site.register(Score)
admin.site.register(AnswerChecker)
admin.site.register(level)


@admin.register(userProfile)
class userProfile(admin.ModelAdmin):
    list_display = [
        'college', 'phone_number', 'user'
    ]
    actions = [csvexport, ]

admin.site.unregister(User)

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [
        'username'
    ]

    actions = [csvexport, ]


@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    # to have a date-based drilldown navigation in the admin page
    date_hierarchy = 'action_time'

    # to filter the resultes by users, content types and action flags
    list_filter = [
        'user',
        'content_type',
        'action_flag'
    ]

    # when searching the user will be able to search in both object_repr and change_message
    search_fields = [
        'object_repr',
        'change_message'
    ]

    list_display = [
        'action_time',
        'user',
        'content_type',
        'action_flag',
    ]
