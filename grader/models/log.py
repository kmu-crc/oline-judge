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


class SubmitLog(models.Model):
    """
    문제:
    S - 솔루션: 입력별 결과가 정해진 문제
    C - 체커: 입력별 결과가 정해지지 않은 문제(CHECKER 프로그램으로 확인)
    F - 따라하기: 문제 내용을 똑같이 따라하는 문제(결과값 없음)
    """
    submit_id = models.IntegerField(
        verbose_name=_('제출정보_ID'),
        db_column='SID',
    )

    problem_id = models.IntegerField(
        verbose_name=_('문제_ID'),
        db_column='PID',
    )

    language_id = models.IntegerField(
        verbose_name=_('언어_ID'),
        db_column='LID',
    )

    code = models.TextField(
        verbose_name=_('제출코드'),
        db_column='CODE',
    )

    result = models.CharField(
        verbose_name=_('결과'),
        db_column='RSLT',
        max_length=10,
        choices=RESULT_TYPE,
        null=True,
        blank=True,
    )

    message = models.TextField(
        verbose_name=_('메시지'),
        db_column='MSG',
        null=True,
        blank=True,
    )

    other_info = models.CharField(
        verbose_name=_('기타정보'),
        db_column='INFO',
        max_length=30,
        null=True,
        blank=True,
    )

    request_time = models.DateTimeField(
        verbose_name=_('요청시간'),
        db_column='RDT',
        auto_now_add=True,
    )

    complete_time = models.DateTimeField(
        verbose_name=_('완료시간'),
        db_column='CDT',
        auto_now=True,
    )

    def __str__(self):
        return '{}_{}'.format(self.submit_id, self.problem_id)

    class Meta:
        db_table = 'SUBMIT_LOG'
        ordering = ['submit_id',]
        verbose_name = _('로그: 제출로그')
        verbose_name_plural = _('로그: 제출로그')
