import os
from django.core.asgi import get_asgi_application

# 환경 변수를 자동으로 감지하고 설정이 없을 경우 기본값 설정
os.environ.setdefault('DJANGO_SETTINGS_MODULE', os.getenv('DJANGO_SETTINGS_MODULE', 'config.settings.production'))

application = get_asgi_application()
