from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password
from django.db import transaction

from ..models.user import User
from ..models.profile import Profile
from ..serializers.user import UserSerializer, UserCreateSerializer


class UserView(APIView):
    authentication_classes = []  # 인증 비활성화
    permission_classes = []      # 권한 검사 비활성화
    
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
        유저 생성 트랜잭션 적용
        """
        serializer = UserCreateSerializer(data=request.data)
        if serializer.is_valid():
            user_data = serializer.validated_data
            user = User.objects.create_user(
                email=user_data['email'],
                password=user_data['password']
            )
            Profile.objects.create(
                id=user,
                nickname=user_data.get('nickname', ''),
                bio=user_data.get('bio', ''),
                platform=user_data.get('platform', '')
            )
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # 트랜잭션 테스트 용 
    # @transaction.atomic
    # def post(self, request):
    #     """
    #     유저 생성 트랜잭션 적용 (테스트용 오류 발생)
    #     """
    #     serializer = UserCreateSerializer(data=request.data)
    #     if serializer.is_valid():
    #         user_data = serializer.validated_data
    #         user = User.objects.create_user(
    #             email=user_data['email'],
    #             password=user_data['password']
    #         )

    #         # ✅ 일부러 오류 발생 (Profile 생성 중 오류 발생)
    #         raise ValueError("강제 오류 발생! 트랜잭션 롤백 테스트")

    #         Profile.objects.create(
    #             user=user,
    #             nickname=user_data.get('nickname', ''),
    #             bio=user_data.get('bio', ''),
    #             platform=user_data.get('platform', '')
    #         )

    #         return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)

    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




## 여기서 부터 검증 필요 ##

class UserDetailView(APIView):
    authentication_classes = []  # 인증 비활성화
    permission_classes = []      # 권한 검사 비활성화

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
        특정 유저 삭제
        """
        user = self.get_object(user_id)
        user.delete()
        return Response({"message": "유저가 삭제되었습니다."}, status=status.HTTP_204_NO_CONTENT)
