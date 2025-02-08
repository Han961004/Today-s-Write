import os

# 환경 변수에서 `DJANGO_SETTINGS_MODULE`을 읽어옴
settings_module = os.getenv('DJANGO_SETTINGS_MODULE', 'config.settings.local')

# 지정된 설정 파일을 가져옴
if settings_module == 'config.settings.production':
    from .production import *
elif settings_module == 'config.settings.local':
    from .local import *
else:
    raise ValueError(f"Invalid DJANGO_SETTINGS_MODULE: {settings_module}")