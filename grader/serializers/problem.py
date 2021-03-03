from rest_framework import serializers

from .. import models


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = ['id', 'category_name']


class TestCaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.TestCase
        fields = ['order', 'input', 'output']


class CheckerSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Checker
        fields = ['language', 'code',]


class ProblemSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Problem
        fields = ['id', 'language', 'name', 'contents', 'time', 'memory', 'case_count', 'problem_type', 'is_open', 'categories']
        read_only_fields = ['language', 'is_open']


class ProblemCreateSerializer(serializers.ModelSerializer):
    language_id = serializers.IntegerField(allow_null=True, required=False)
    testcase = TestCaseSerializer(source='testcase_set', many=True)
    checker = CheckerSerializer(allow_null=True, required=False)

    class Meta:
        model = models.Problem
        fields = ['id', 'language_id', 'name', 'contents', 'template', 'time', 'memory', 'case_count', 'problem_type',
                  'testcase', 'checker', 'categories']


    def validate(self, attrs):
        if (attrs['problem_type'] in ['S', 'F']) and 'checker' in attrs:
            raise serializers.ValidationError({
                'code': ['데이터 구성이 올바르지 않습니다.',
                         '불필요한 CHECKER 프로그램이 작성됐습니다.']
            })

        elif attrs['problem_type'] == 'C':
            if 'checker' not in attrs:
                raise serializers.ValidationError({
                    'code': ['데이터 구성이 올바르지 않습니다.',
                             'CHECKER 프로그램이 작성되지 않았습니다.']
                })
            for case in attrs['testcase_set']:
                if 'output' in case:
                    raise serializers.ValidationError({
                        'code': ['데이터 구성이 올바르지 않습니다.',
                                 '불필요한 testcase가 작성됐습니다.']
                    })

        elif attrs['problem_type'] == 'F':
            if len(attrs['testcase_set']) > 1 or 'input' in attrs['testcase_set'][0]:
                raise serializers.ValidationError({
                    'code': ['데이터 구성이 올바르지 않습니다.',
                             '불필요한 testcase가 작성됐습니다.']
                })

        return super(ProblemCreateSerializer, self).validate(attrs)
