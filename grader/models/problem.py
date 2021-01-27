from django.db import models
from django.utils.translation import ugettext as _

from .language import Language


PROBLEM_TYPE = (
    ('S', '솔루션'),
    ('C', '체커'),
    ('F', '따라하기')
)

class Problem(models.Model):
    """
    문제:
    S - 솔루션: 입력별 결과가 정해진 문제
    C - 체커: 입력별 결과가 정해지지 않은 문제(CHECKER 프로그램으로 확인)
    F - 따라하기: 문제 내용을 똑같이 따라하는 문제(결과값 없음)
    """
    language = models.ForeignKey(
        Language,
        verbose_name=_('언어'),
        db_column='LANG',
        primary_key=False,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
    )

    name = models.CharField(
        verbose_name=_('이름'),
        db_column='NAME',
        max_length=50,
    )

    contents = models.TextField(
        verbose_name=_('내용'),
        db_column='CTS',
    )

    time = models.PositiveSmallIntegerField(
        verbose_name=_('제한시간(ms)'),
        db_column='TIME',
    )

    memory = models.PositiveSmallIntegerField(
        verbose_name=_('제한메모리(MB)'),
        db_column='MRY',
    )

    problem_type = models.CharField(
        verbose_name=_('문제타입'),
        db_column='PTYP',
        max_length=1,
        choices=PROBLEM_TYPE,
    )

    categories = models.ManyToManyField(
        'Category',
        verbose_name = _('분류'),
        db_column = 'CATS',
        null=True,
        blank=True,
    )

    is_open = models.BooleanField(
        verbose_name=_('문제공개'),
        db_column='OPEN',
        null=True,
        default=False,
    )

    def __str__(self):
        return '{}_{}'.format(self.name, self.problem_type)

    class Meta:
        db_table = 'PROBLEM'
        ordering = ['id',]
        verbose_name = _('문제: 문제')
        verbose_name_plural = _('문제: 문제')


class TestCase(models.Model):
    """
    테스트케이스:
    S: 입력/출력 모두 존재
    C: 입력만 존재
    F: 출력만 존재
    """
    problem = models.ForeignKey(
        Problem,
        verbose_name=_('문제'),
        db_column='PRBM',
        primary_key=False,
        on_delete=models.CASCADE,
    )

    order = models.PositiveSmallIntegerField(
        verbose_name=_('순서'),
        db_column='ODR',
        primary_key=False,
    )

    input = models.TextField(
        verbose_name=_('입력'),
        db_column='IN',
        null=True,
        blank=True,
    )

    output = models.TextField(
        verbose_name=_('출력'),
        db_column='OUT',
        null=True,
        blank=True,
    )

    def __str__(self):
        return '{}-TEST_CASE'.format(self.problem.name)

    class Meta:
        db_table = 'TEST_CASE'
        ordering = ['problem', 'order']
        unique_together = (('problem', 'order'),)
        verbose_name = _('문제: 테스트케이스')
        verbose_name_plural = _('문제: 테스트케이스')


class Checker(models.Model):
    """
    체커:
    문제타입이 C인 경우만 존재
    """
    problem = models.ForeignKey(
        Problem,
        verbose_name=_('문제'),
        db_column='PRBM',
        unique=True,
        primary_key=False,
        on_delete=models.CASCADE,
    )

    language = models.ForeignKey(
        Language,
        verbose_name=_('언어'),
        db_column='LANG',
        primary_key=False,
        on_delete=models.CASCADE,
    )

    code = models.TextField(
        verbose_name=_('코드'),
        db_column='CODE',
    )

    def __str__(self):
        return '{}-CHECKER'.format(self.problem.name)

    class Meta:
        db_table = 'CHECKER'
        ordering = ['problem']
        verbose_name = _('문제: 체커')
        verbose_name_plural = _('문제: 체커')