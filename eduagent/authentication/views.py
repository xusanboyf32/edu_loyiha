# authentication/views.py

from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import  IsAuthenticated

from .serializers import  UserSerializer


class CheckAuthView(APIView):
    """
    Vazifa: User login qilganmi tekshirish
    Natija: Frontend user holatini biladi
    """

    def get(self, request):
        if request.user.is_authenticated:
            return Response({
                'authenticated': True,
                'user': UserSerializer(request.user).data
            })
        return Response({'authenticated': False})


class LogoutView(APIView):
    """
    Vazifa: User ni logout qilish
    Natija: Session tozalanishi
    """

    def post(self, request):
        from django.contrib.auth import logout
        logout(request)
        return Response({'success': True, 'message': 'Logged out'})


# ==================== ADMIN VIEWS ====================
class AdminCreateUserView(APIView):
    """
    Vazifa: Admin yangi user yaratish
    Natija: Parolsiz user yaratiladi
    """
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Faqat adminlar user yarata oladi
        if request.user.role not in [CustomUser.ROLE_ADMIN, CustomUser.ROLE_SUPERADMIN]:
            return Response(
                {'error': 'Ruxsat yo\'q'},
                status=status.HTTP_403_FORBIDDEN
            )

        phone_number = request.data.get('phone_number')
        role = request.data.get('role', CustomUser.ROLE_STUDENT)
        first_name = request.data.get('first_name', '')
        last_name = request.data.get('last_name', '')

        if not phone_number:
            return Response(
                {'error': 'Telefon raqam kiritilishi kerak'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # User yaratish (PAROL BERILMAYDI!)
        try:
            user = CustomUser.objects.create_user(
                phone_number=phone_number,
                role=role,
                first_name=first_name,
                last_name=last_name
            )

            return Response({
                'success': True,
                'message': f'Foydalanuvchi yaratildi: {phone_number}',
                'user': UserSerializer(user).data
            })

        except Exception as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )



# =============================================================================================
# =============================================================================================
 #  BU BOTDAN AUTH BOLISH UHCUN VIEW MODEL BN VIEW YETARLI
# =============================================================================================

# authentication/views.py
from django.http import JsonResponse
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login
from django.utils import timezone
from .models import CustomUser, TelegramAuth

@csrf_exempt
def telegram_callback(request):
    # Telegram start link GET so'rovi
    if request.method == "GET":
        session_token = request.GET.get("token")
        code = request.GET.get("code")

        if not session_token or not code:
            return JsonResponse({"success":False,"message":"Token yoki kod topilmadi."},status=400)
        try:
            # is_used holatini e'tiborsiz qoldiramiz, faqat token va kodni tekshiramiz
            auth = TelegramAuth.objects.get(session_token=session_token, code=code)

            if auth.is_expired:
                return JsonResponse({"success":False,"message":"Kod muddatli o'tgan."},status=400)

            # Agar allaqachon ishlatilgan bo'lsa ham , muddati tugamagan bolsa ruxsat beramiz
            if auth.is_used:
                print(f"[WARNING] Auth {session_token} allaqachon ishlatilgan, lekin muddati hali tugamagan")

            user, created = CustomUser.objects.get_or_create(
                phone_number=auth.phone_number,
                defaults={'role':CustomUser.ROLE_STUDENT}  # ROLE STUDENT

            )

            # Telegram ma'lumotlar yangilash
            user.telegram_id = auth.chat_id
            user.is_verified = True
            user.verified_at = timezone.now()
            user.save()

            # Auth ishlatilgan deb belgilash

            auth.is_used = True
            auth.save()

            #Django sessionga login qilish
            if not request.session.session_key:
                request.session.create()
            request.session.save()
            auth_login(request, user)

            return redirect('home')

        except TelegramAuth.DoesNotExist:
            return JsonResponse({"success":False,"message":"Noto'g'ri kod yoki sessiya."},status=400)
    return JsonResponse({"success":False,"message":"Noto'g'ri so'rov turi"},status=400)




