from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.viewsets import mixins as mx
from django_filters import rest_framework as filters

from grader import serializers
from grader import models


class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CategorySerializer
    queryset = models.Category.objects.all()
    ordering = ['-id']
    lookup_url_kwarg = 'id'
