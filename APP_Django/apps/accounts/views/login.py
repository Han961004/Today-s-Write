from django.contrib.auth import authenticate, login
from rest_framework import permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework_simplejwt.tokens import RefreshToken  # JWT 토큰을 위해 추가
from ..serializers.user import *


class LoginView(APIView):
    authentication_classes = []  # 인증 비활성화
    permission_classes = []      # 권한 검사 비활성화
    
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']  # user를 validated_data에서 가져옵니다.
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            # JWT 토큰 생성 (access_token, refresh_token)
            refresh = RefreshToken.for_user(user)
            return Response({
                "email": user.email,
                "access_token": str(refresh.access_token),  # access_token 반환
                "refresh_token": str(refresh),  # refresh_token 반환
            }, status=status.HTTP_200_OK)

            
        return Response({"detail": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
