from django.db import models
from django.utils.translation import ugettext as _

from .problem import Problem


RESULT_TYPE = (
    ('S', '성공'),
    ('F', '실패'),
    ('T', '시간초과'),
    ('M', '메모리초과'),
    ('C', '컴파일에러'),
    ('R', '런타임에러'),
    ('E', '서버에러'),
    ('P', '문제에러'),
)


class Category(models.Model):
    """
    분류항목
    """
    category_name = models.CharField(
        verbose_name=_('분류명'),
        db_column='NAME',
        max_length=10,
        unique=True,
    )

    def __str__(self):
        return self.category_name

    class Meta:
        db_table = 'CATEGORY'
        ordering = ['id',]
        verbose_name = _('분류: 분류항목')
        verbose_name_plural = _('분류: 분류항목')
