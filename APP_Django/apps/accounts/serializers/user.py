from rest_framework import serializers
from django.contrib.auth import authenticate

from ..models.user import User


class UserSerializer(serializers.ModelSerializer):
    """
    User 모델 직렬화
    """
    class Meta:
        model = User
        fields = '__all__'

class UserCreateSerializer(serializers.Serializer):
    """
    User 생성 요청 데이터를 검증하고 직렬화
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True, min_length=8)
    nickname = serializers.CharField(write_only=True, required=False, allow_blank=True)

    def validate_email(self, value):
        """
        이메일 중복 검사
        """
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("이미 사용 중인 이메일입니다.")
        return value

class UserLoginSerializer(serializers.Serializer):
    """
    User 로그인 요청 데이터를 검증하고 직렬화
    """
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        """
        email과 password로 사용자 인증
        """
        email = data['email']
        password = data['password']

        # DB 쿼리 최적화: 필요한 필드만 가져오기
        user = User.objects.filter(email=email).only("id", "password").first()
        if not user or not user.check_password(password):  # authenticate() 없이 직접 검증
            raise serializers.ValidationError("유효하지 않은 자격 증명입니다.")

        data['user'] = user
        return data
