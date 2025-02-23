from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.db import transaction
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.accounts.models.user import User
from apps.accounts.models.profile import Profile
from apps.accounts.serializers.user import UserSerializer, UserCreateSerializer
from apps.accounts.serializers.profile import ProfileSerializer, ProfileUpdateSerializer


class UserView(APIView):
    authentication_classes = []
    permission_classes = []

    def get(self, request):
        """
        유저 전체 리스트 조회
        """
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @transaction.atomic
    def post(self, request):
        """
        Transaction을 이용하여 User와 Profile 동시 생성
        """
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            user = User.objects.create_user(
                email=user_data['email'],
                password=user_data['password']
            )
            Profile.objects.create(
                id=user,  # User와 1:1 관계로 연결되어 있다고 가정
                nickname=user_data.get('nickname', ''),
                bio=user_data.get('bio', ''),
                platform=user_data.get('platform', '')
            )
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserDetailView(APIView):
    authentication_classes = [] 
    permission_classes = [] 

    def get_object(self, user_id):
        return get_object_or_404(User, id=user_id)

    def get(self, request, user_id):
        """
        특정 유저 조회
        """
        user = self.get_object(user_id)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, user_id):
        """
        특정 유저 정보 수정
        """
        user = self.get_object(user_id)
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user.email = serializer.validated_data['email']
            user.password = make_password(serializer.validated_data['password'])
            user.save()
            return Response(UserSerializer(user).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, user_id):
        """
        특정 유저 삭제 (연결된 Profile은 cascade 설정에 따라 함께 삭제)
        """
        user = self.get_object(user_id)
        user.delete()
        return Response({"message": "유저가 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)


# 모든 프로필 조회
class ProfileView(APIView):
    def get(self, request):
        """
        프로필 목록 조회
        """
        profiles = Profile.objects.all()
        return Response(ProfileSerializer(profiles, many=True).data)


# 특정 프로필에 대한 조회 및 수정
class ProfileDetailView(APIView):
    def get(self, request, profile_id):
        """
        프로필 상세 조회 (자신의 프로필만 조회 가능)
        """
        profile = get_object_or_404(Profile, pk=profile_id)
        if profile.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        return Response(ProfileSerializer(profile).data)

    def put(self, request, profile_id):
        """
        인증된 사용자의 프로필 전체 업데이트
        """
        profile = get_object_or_404(Profile, pk=profile_id)
        if profile.user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

        serializer = ProfileUpdateSerializer(data=request.data)
        if serializer.is_valid():
            validated_data = serializer.validated_data
            # 검증된 데이터를 사용하여 프로필 인스턴스 업데이트
            for attr, value in validated_data.items():
                setattr(profile, attr, value)
            profile.save()
            return Response(ProfileSerializer(profile).data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
