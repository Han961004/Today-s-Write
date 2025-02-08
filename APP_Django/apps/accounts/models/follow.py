from django.db import models
from django.conf import settings


class Follow(models.Model):
    """
    내가 팔로우, 나를 팔로우, 팔로우한 시간
    """
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='following', on_delete=models.CASCADE)
    followed = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('follower', 'followed')  # 동일한 팔로우 관계 중복 방지