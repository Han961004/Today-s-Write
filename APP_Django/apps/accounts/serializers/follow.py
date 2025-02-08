from rest_framework import serializers
from ..models import Follow, Profile


class FollowSerializer(serializers.ModelSerializer):
    """
    팔로우 직렬화
    """
    class Meta:
        model = Follow
        fields = '__all__'
        
    def validate(self, attrs):
        """
        팔로우 관계에 대한 검증
        """
        follower = attrs.get('follower')
        followed = attrs.get('followed')

        if follower == followed:
            raise serializers.ValidationError("사용자는 자신을 팔로우할 수 없습니다.")

        if Follow.objects.filter(follower=follower, followed=followed).exists():
            raise serializers.ValidationError("이미 팔로우 관계가 존재합니다.")

        return attrs