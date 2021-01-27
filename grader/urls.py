import re

from django.conf import settings
from django.conf.urls import url, include
from django.urls import re_path, path
from rest_framework import permissions, authentication

from . import views, routers

from drf_yasg.views import get_schema_view
from drf_yasg import openapi


router = routers.AppRouter()
router.register(r'language', views.api.LanguageViewSet, basename='language')
router.register(r'problem/treat', views.api.ProblemViewSet, basename='problem-treat')
router.register(r'problem', views.api.GetProblemViewSet, basename='problem')
router.register(r'submit', views.api.SubmitViewSet, basename='submit')
router.register(r'category', views.api.CategoryViewSet, basename='category')



v1_api_info = openapi.Info(
    title="Grader API 문서",
    default_version="v1",
    description="Grader API 문서화",
    contact=openapi.Contact(email="admin@admin.com"),
)
v1_schema_view = get_schema_view(
    v1_api_info,
    public=True,
    # permission_classes=(
    #     permissions.IsAdminUser,
    # ),
)

_cache_timeout = 0 if settings.DEBUG else 3600
urlpatterns = [
    url(r'^', include(router.urls)),
    # 온라인 API 문서화
    re_path(r"^swagger(?P<format>.json|.yaml)$", v1_schema_view.without_ui(cache_timeout=_cache_timeout),
            name="schema-json"),
    re_path(r"^swagger/?$", v1_schema_view.with_ui("swagger", cache_timeout=_cache_timeout),
            name="schema-swagger-ui"),
    path("v1", v1_schema_view.with_ui("redoc", cache_timeout=_cache_timeout), name="schema-redoc"),
]
