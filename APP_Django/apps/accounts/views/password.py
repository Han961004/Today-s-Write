from django.core.mail import send_mail
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import permissions

from ..models import User

class PasswordResetView(APIView):
    """
    패스워드 초기화를 위한 View
    """
    authentication_classes = []
    permission_classes = []

    def post(self, request):
        email = request.data.get("email")
        user = User.objects.filter(email=email).first()
        if not user:
            return Response({"detail": "해당 이메일이 존재하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 패스워드 재설정을 위한 JWT 토큰 생성
        reset_token = RefreshToken.for_user(user)
        reset_link = f"{request.build_absolute_uri('/reset-password/')}?token={str(reset_token.access_token)}"

        # 이메일 발송
        send_mail(
            subject="패스워드 초기화 요청",
            message=f"다음 링크를 통해 패스워드를 초기화하세요: {reset_link}",
            from_email="no-reply@example.com",
            recipient_list=[email],
        )

        return Response({"message": "패스워드 초기화 이메일이 발송되었습니다."}, status=status.HTTP_200_OK)

class PasswordChangeView(APIView):
    """
    패스워드 변경을 위한 View
    """
    permission_classes = [permissions.IsAuthenticated]

    def put(self, request):
        user = request.user
        old_password = request.data.get("old_password")
        new_password = request.data.get("new_password")

        # 기존 비밀번호 확인
        if not user.check_password(old_password):
            return Response({"detail": "기존 비밀번호가 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 새로운 비밀번호 저장
        user.set_password(new_password)
        user.save()
        return Response({"message": "비밀번호가 성공적으로 변경되었습니다."}, status=status.HTTP_200_OK)
