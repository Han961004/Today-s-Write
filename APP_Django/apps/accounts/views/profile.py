from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.accounts.models.profile import Profile
from apps.accounts.serializers.profile import *
from apps.accounts.serializers.user import *


class ProfileView(APIView):

    def get(self, request):
        """
        프로필 목록
        """
        profiles = Profile.objects.all()
        return Response(ProfileSerializer(profiles, many=True).data)
    
class ProfileDetailView(APIView):
    
    def get(self, request, profile_id):
        """
        아아디로 프로필 조회
        """
        profile = get_object_or_404(Profile, pk=profile_id)
        if profile.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(ProfileSerializer(profile).data)

    def put(self, request, profile_id):
        """
        update the entire profile of authenticated user
        """
        profile = get_object_or_404(Profile, pk=profile_id)
        if profile.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = ProfileUpdateSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # 검증된 데이터를 사용하여 프로필 인스턴스를 업데이트
            for attr, value in validated_data.items():
                setattr(profile, attr, value)
                """
                setattr(profile, "nickname", "new_nickname")  # profile.nickname = "new_nickname"
                setattr(profile, "bio", "Updated bio")        # profile.bio = "Updated bio"
                setattr(profile, "platform", "web")           # profile.platform = "web"
                """
            profile.save()
            return Response(ProfileSerializer(profile).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)