from django.db import models
from django.utils.translation import ugettext as _


class Language(models.Model):
    name = models.CharField(
        verbose_name=_('이름'),
        db_column='NAME',
        max_length=15,
    )

    extension = models.CharField(
        verbose_name=_('확장자'),
        db_column='EXT',
        max_length=5,
    )

    compile_path = models.TextField(
        verbose_name=_('컴파일러 경로'),
        db_column='CPT',
    )

    compile_command = models.TextField(
        verbose_name=_('컴파일 명령어'),
        db_column='CCM',
    )

    run_path = models.TextField(
        verbose_name=_('실행 경로'),
        db_column='RPT',
        null=True,
        blank=True,
    )

    run_command = models.TextField(
        verbose_name=_('실행 명령어'),
        db_column='RCM',
    )

    creation_date = models.DateTimeField(
        verbose_name=_('생성일'),
        db_column='CDT',
        auto_now_add=True,
    )

    update_date = models.DateTimeField(
        verbose_name=_('수정일'),
        db_column='UDT',
        auto_now=True,
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'LANGUAGE'
        ordering = ['id',]
        verbose_name = _('언어: 언어')
        verbose_name_plural = _('언어: 언어')