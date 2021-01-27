from rest_framework import serializers

from .. import models


class LanguageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Language
        fields = ['id', 'name', 'extension', 'compile_path', 'compile_command',
                  'run_path', 'run_command']
