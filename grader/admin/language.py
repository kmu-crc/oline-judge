from django.contrib import admin

from .. import models


@admin.register(models.Language)
class LanguageAdmin(admin.ModelAdmin):
    """
    언어 관리
    """
    list_display = ['name', 'extension', 'compile_path', 'compile_command',
                    'run_path', 'run_command', 'creation_date', 'update_date']
    list_filter = ['name',]
    search_fields = ['name',]
    list_per_page = 30

    class Meta:
        model = models.Language
