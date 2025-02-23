from django.contrib import admin
from django.urls import path, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django_prometheus.exports import ExportToDjangoView

from apps.accounts.views.login import LoginView
from APP_Django.apps.accounts.views.accounts import *

schema_view = get_schema_view(
    openapi.Info(
        title="Literature API",
        default_version='v1.0.0',
        description="문학 및 사용자 관리 API 문서",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="your_email@example.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

def trigger_error(request):
    division_by_zero = 1 / 0

urlpatterns = [
    path('admin/', admin.site.urls),
    path("metrics/", ExportToDjangoView),  # 올바른 Prometheus 엔드포인트
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('sentry-debug/', trigger_error),

    
    # home
    # path('', ),
    
    # accounts
    path('accounts/create/', UserView.as_view()),
    path('accounts/login/', LoginView.as_view()),
    
]
