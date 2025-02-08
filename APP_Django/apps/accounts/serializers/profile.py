from rest_framework import serializers
from ..models.profile import Profile


class ProfileSerializer(serializers.ModelSerializer):
    """
    Profile 데이터를 직렬화
    """
    class Meta:
        model = Profile
        fields = '__all__'

class ProfileUpdateSerializer(serializers.Serializer):
    """
    Profile 업데이트 요청 데이터를 검증
    """
    nickname = serializers.CharField(max_length=10, required=False, allow_blank=True)
    bio = serializers.CharField(max_length=50, required=False, allow_blank=True)
    platform = serializers.CharField(max_length=10, required=False, allow_blank=True)

    def validate_nickname(self, value):
        """
        닉네임 검증: 중복 닉네임 방지
        """
        if Profile.objects.filter(nickname=value).exists():
            raise serializers.ValidationError("이미 존재하는 닉네임입니다.")
        return value