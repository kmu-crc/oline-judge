from django.db.models import Q
from django.utils.translation import ugettext as _
from django_filters import rest_framework as filters

from .. import models


class NumberInFilter(filters.BaseInFilter, filters.NumberFilter, filters.MultipleChoiceFilter):
    pass


class ProblemFilter(filters.FilterSet):
    language = filters.NumberFilter(label=_('언어 ID'), field_name='language',
                                  help_text=_('조회할 언어 ID'), method='language_filter')
    categories = filters.AllValuesMultipleFilter(label=_('분류항목 ID'), field_name='categories',
                                                 help_text=_('조회할 분류항목 ID 목록'))

    class Meta:
        model = models.Problem
        fields = ['categories', 'language']

    def language_filter(self, queryset, name, value):
        return queryset.filter(Q(language=value) | Q(language=None))