from django.contrib import admin

from .. import models


@admin.register(models.Category)
class CategoryAdmin(admin.ModelAdmin):
    """
    분류항목 관리
    """
    list_display = ['category_name']
    list_filter = ['category_name',]
    search_fields = ['category_name',]
    list_per_page = 30

    class Meta:
        model = models.Category
