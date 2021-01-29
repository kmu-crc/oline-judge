from django.utils.decorators import method_decorator
from rest_framework.viewsets import mixins as mx
from rest_framework import viewsets, status
from rest_framework.response import Response

from drf_yasg.utils import swagger_auto_schema

from grader import serializers
from grader import models

from grader.tasks.grade_celery import grade_code, check_task_order


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="""
    제출된 코드의 채점 요청.
    + submit_id - 플랫폼의 제출 ID,
    + problem_id - 문제 ID,
    + language_id - 사용된 언어 ID,
    + code - 채점할 코드
    
    Response
    + \+ order - 채점 순서 (처리 대기중인 채점 요청 개수)
    """
))
class SubmitViewSet(mx.CreateModelMixin,
                    mx.UpdateModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = serializers.SubmitSerializer
    queryset = models.SubmitLog.objects.all()
    ordering = ['-id']
    lookup_url_kwarg = 'id'

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        instance = models.SubmitLog.objects.create(**{
            'submit_id': data['submit_id'],
            'problem_id': data['problem_id'],
            'language_id': data['language_id'],
            'code': data['submitlog_code'][0],
        })
        data.setdefault('log_id', instance.id)

        order = check_task_order()

        grade_code.delay(**data)

        data.setdefault('order', order + 1)
        headers = self.get_success_headers(data)
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        instance = models.SubmitLog.objects.get(id=kwargs[self.lookup_url_kwarg])
        serializer = serializers.SubmitLogSerializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        serializer.save()
        return Response(status.HTTP_200_OK)
