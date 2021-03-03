from django.contrib import admin

from .. import models


@admin.register(models.Problem)
class ProblemAdmin(admin.ModelAdmin):
    """
    문제 관리
    """
    list_display = ['language', 'name', 'contents', 'time', 'memory', 'case_count', 'problem_type', 'template']
    filter_horizontal = ['categories',]
    list_filter = ['language', 'name', 'problem_type']
    search_fields = ['language', 'name', 'problem_type']
    list_per_page = 30

    list_select_related = ['language', ]

    class Meta:
        model = models.Problem


@admin.register(models.TestCase)
class TestCaseAdmin(admin.ModelAdmin):
    """
    테스트케이스 관리
    """
    list_display = ['problem', 'input', 'output']
    list_filter = ['problem',]
    search_fields = ['problem',]
    list_per_page = 30

    list_select_related = ['problem', ]

    class Meta:
        model = models.TestCase


@admin.register(models.Checker)
class CheckerAdmin(admin.ModelAdmin):
    """
    체커 관리
    """
    list_display = ['problem', 'language', 'code']
    list_filter = ['problem', 'language']
    search_fields = ['problem', 'language']
    list_per_page = 30

    list_select_related = ['problem', 'language', ]

    class Meta:
        model = models.Checker