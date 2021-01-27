from rest_framework import serializers

from grader import models


class SubmitSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.SubmitLog
        fields = ['submit_id', 'problem_id', 'language_id', 'code', 'order']


class SubmitLogSerializer(serializers.ModelSerializer):
    order = serializers.IntegerField(read_only=True)

    class Meta:
        model = models.SubmitLog
        fields = ['submit_id', 'problem_id', 'language_id', 'code', 'order', 'result', 'message', 'other_info']