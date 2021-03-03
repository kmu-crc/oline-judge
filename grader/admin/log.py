from django.contrib import admin

from .. import models


@admin.register(models.SubmitLog)
class SubmitLogAdmin(admin.ModelAdmin):
    """
    제출 로그 관리
    """
    def ref_request_time(self, instance):
        return instance.request_time.astimezone().strftime('%Y년 %m월 %d일 %H:%M:%S')
    ref_request_time.short_description = '요청시간'
    ref_request_time.admin_order_field = 'request_time'

    def ref_complete_time(self, instance):
        return instance.complete_time.astimezone().strftime('%Y년 %m월 %d일 %H:%M:%S')
    ref_complete_time.short_description = '완료시간'
    ref_complete_time.admin_order_field = 'complete_time'

    list_display = ['submit_id', 'problem_id', 'language_id', 'result', 'ref_request_time', 'ref_complete_time',]
    list_filter = ['submit_id', 'problem_id', 'language_id',]
    search_fields = ['submit_id', 'problem_id', 'language_id',]
    list_per_page = 30

    class Meta:
        model = models.SubmitLog
