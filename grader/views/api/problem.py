from rest_framework.decorators import action
from rest_framework.viewsets import mixins as mx
from rest_framework import viewsets
from rest_framework.response import Response
from django.db import transaction
from django.utils.decorators import method_decorator

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema, no_body

from grader import serializers
from grader import models
from grader.filters import ProblemFilter

from grader.tasks.grade_celery import grade_code


class GetProblemViewSet(mx.ListModelMixin,
                        mx.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    serializer_class = serializers.ProblemSerializer
    queryset = models.Problem.objects.all()
    ordering = ['-id']
    filterset_class = ProblemFilter
    lookup_url_kwarg = 'id'

    def get_queryset(self):
        qs = super(GetProblemViewSet, self).get_queryset()
        if self.action == 'testcase':
            qs = qs.filter(**{
                self.lookup_field: self.kwargs[self.lookup_url_kwarg],
            })
        return qs

    @action(detail=False, methods=['GET'],
            url_path=r'(?P<id>[0-9]+)/testcase',
            url_name='testcase',
            lookup_field='problem_id',
            lookup_url_kwarg='id',
            filterset_class=None,
            queryset=models.TestCase.objects.all(),
            serializer_class=serializers.TestCaseSerializer)
    def testcase(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    @action(detail=True, methods=['GET'],
            url_path=r'checker',
            url_name='checker',
            lookup_field='problem_id',
            lookup_url_kwarg='id',
            filterset_class=None,
            queryset=models.Checker.objects.all(),
            serializer_class=serializers.CheckerSerializer)
    def checker(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)


@method_decorator(name='create', decorator=swagger_auto_schema(
    operation_description="""
    문제 생성 요청.
    + language_id - 언어 ID => 특정 언어에 한정된 문제인 경우에만 작성,
    + name - 문제이름,
    + contents - 문제 pdf 파일 경로 => 추후 텍스트 작성 가능,
    + template - 템플릿 코드,
    + time - 제한시간(ms)
    + memory - 제한메모리(MB)
    + case_count - 채점 시 사용할 테스트케이스 개수
    + problem_type - 문제타입 => [S,C,F]
    \t+ Solution(S) - 입력에 대한 출력이 고정된 문제
    \t+ Checker(C) - 입력에 대한 출력이 고정되지 않은 문제
    \t+ Follow(F) - 주어진 예제를 똑같이 따라하는 문제
    + testcase - order(채점 순서), input(입력), output(출력)
    1개 이상 리스트 형태로 작성. 문제타입에 따라 작성방법이 다름.
    \t+ S - 일반적으로 입력과 출력을 모두 작성. 단순 출력 문제의 경우 출력만 작성. 
    \t+ C - 입력만 작성
    \t+ F - 출력만 작성
    + checker - 문제타입이 'C'인 경우만 작성.
    + categories - 문제 태그. 리스트 형태로 작성.
    """
))
class ProblemViewSet(mx.CreateModelMixin,
                     mx.UpdateModelMixin,
                     mx.DestroyModelMixin,
                     viewsets.GenericViewSet):
    serializer_class = serializers.ProblemCreateSerializer
    queryset = models.Problem.objects.all()
    ordering = ['-id']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        categories = serializer.validated_data.pop('categories')

        checker = None
        testcase = serializer.validated_data.pop('testcase_set')
        if 'checker' in serializer.validated_data:
            checker = serializer.validated_data.pop('checker')

        with transaction.atomic():
            instance = models.Problem.objects.create(**serializer.validated_data)
            instance.categories.add(*categories)

            if checker:
                checker.setdefault('problem', instance)
                models.Checker.objects.create(**checker)

            for case in testcase:
                case.setdefault('problem', instance)
                models.TestCase.objects.create(**case)

        serializer = self.serializer_class(instance)
        return Response(serializer.data)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        categories = serializer.validated_data.pop('categories')

        checker = None
        testcase = serializer.validated_data.pop('testcase_set')
        if 'checker' in serializer.validated_data:
            checker = serializer.validated_data.pop('checker')

        with transaction.atomic():
            models.Problem.objects.filter(id=kwargs['pk']).update(**serializer.validated_data)
            if checker:
                models.Checker.objects.filter(problem_id=kwargs['pk']).update(**checker)

            models.TestCase.objects.filter(problem_id=kwargs['pk']).delete()
            for case in testcase:
                case.setdefault('problem_id', kwargs['pk'])
                models.TestCase.objects.create(**case)

            instance = models.Problem.objects.get(id=kwargs['pk'])
            instance.categories.clear()
            instance.categories.add(*categories)


        serializer = self.serializer_class(instance)
        return Response(serializer.data)
