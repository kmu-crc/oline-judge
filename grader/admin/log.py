from django.contrib import admin

from .. import models


@admin.register(models.SubmitLog)
class SubmitLogAdmin(admin.ModelAdmin):
    """
    제출 로그 관리
    """
    list_display = ['submit_id', 'problem_id', 'language_id', 'result', 'request_time', 'complete_time',]
    list_filter = ['submit_id', 'problem_id', 'language_id',]
    search_fields = ['submit_id', 'problem_id', 'language_id',]
    list_per_page = 30

    class Meta:
        model = models.SubmitLog
