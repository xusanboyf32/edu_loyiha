from django.shortcuts import render, redirect  # Add render here
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from .models import CustomUser, TelegramAuth
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .serializers import UserSerializer
import secrets
from django.utils import timezone
from django.conf import settings

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
#   BU BOTDAN AUTH BOLISH UHCUN VIEW MODEL BN VIEW YETARLI
# =============================================================================================

from django.http import JsonResponse
from django.contrib.auth import login as auth_login
from django.contrib import messages
# authentication/views.py
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.contrib.auth import login as auth_login, logout
from django.utils import timezone
from .models import CustomUser, TelegramAuth

def telegram_callback(request):
    # Get the auth data from Telegram
    auth_data = request.GET.dict()
    
    # Verify the required parameters are present
    required_params = ['id', 'first_name', 'auth_date', 'hash']
    if not all(param in auth_data for param in required_params):
        return redirect('login')
    
    # Here you should:
    # 1. Verify the auth_data hash using your bot token
    # 2. Get or create a user based on the Telegram ID
    # 3. Log the user in
    
    # For now, let's just show the auth data
    return JsonResponse(auth_data)


# ==================== TELEGRAM AUTH VIEWS ====================
@csrf_exempt
def telegram_auth_start(request):
    """
    Vazifa: Telegram auth uchun session token yaratish
    Natija: Frontend ga session token va bot username qaytaradi
    """
    if request.method == 'POST':
        try:
            # Generate unique session token
            session_token = secrets.token_urlsafe(9)
            
            # Create TelegramAuth record
            telegram_auth = TelegramAuth.objects.create(
                session_token=session_token,
                expires_at=timezone.now() + timezone.timedelta(minutes=10),
                chat_id='pending'
            )
            
            return JsonResponse({
                'success': True,
                'session_token': session_token,
                'bot_username': getattr(settings, 'TELEGRAM_BOT_USERNAME', 'your_bot_username'),
                'expires_in': 600  # 10 minutes
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': str(e)
            }, status=500)
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


@csrf_exempt
def telegram_auth_verify(request):
    """
    Vazifa: Telegram orqali kelgan kodni tekshirish
    Natija: User ni tizimga kiradi yoki xatolik qaytaradi
    """
    if request.method == 'POST':
        try:
            data = request.GET if request.content_type == 'text/plain' else request.POST
            if hasattr(request, 'body') and request.content_type == 'application/json':
                import json
                data = json.loads(request.body.decode('utf-8'))
            
            session_token = data.get('session_token')
            code = data.get('code')
            
            if not session_token or not code:
                return JsonResponse({
                    'success': False,
                    'error': 'Session token va code kerak'
                }, status=400)
            
            # Get TelegramAuth record
            try:
                telegram_auth = TelegramAuth.objects.get(
                    session_token=session_token,
                    code=code,
                    is_used=False
                )
            except TelegramAuth.DoesNotExist:
                return JsonResponse({
                    'success': False,
                    'error': 'Noto\'g\'ri kod yoki sessiya'
                }, status=400)
            
            # Check if expired
            if telegram_auth.is_expired:
                return JsonResponse({
                    'success': False,
                    'error': 'Sessiya muddati o\'tgan'
                }, status=400)
            
            # Get or create user
            user = None
            if telegram_auth.phone_number:
                try:
                    user = CustomUser.objects.get(phone_number=telegram_auth.phone_number)
                except CustomUser.DoesNotExist:
                    # Create new user if not exists
                    user = CustomUser.objects.create_user(
                        phone_number=telegram_auth.phone_number,
                        first_name='Telegram',
                        last_name='User'
                    )
            
            if not user:
                return JsonResponse({
                    'success': False,
                    'error': 'Foydalanuvchi topilmadi'
                }, status=400)
            
            # Mark as used
            telegram_auth.is_used = True
            telegram_auth.save()
            
            # Login user
            auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
            return JsonResponse({
                'success': True,
                'message': 'Muvaffaqiyatli kirish!',
                'redirect_url': '/',
                'user': {
                    'id': user.id,
                    'phone_number': user.phone_number,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'role': user.role
                }
            })
            
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'Xatolik: {str(e)}'
            }, status=500)
    
    return JsonResponse({'success': False, 'error': 'Method not allowed'}, status=405)


@csrf_exempt
def telegram_webhook(request):
    """
    Vazifa: Telegram botdan webhook qabul qilish
    Natija: Kodni saqlaydi va user ni tasdiqlaydi
    """
    if request.method == 'POST':
        try:
            import json
            data = json.loads(request.body.decode('utf-8'))
            
            # Handle webhook data from Telegram bot
            # This would handle the code verification from bot
            
            return JsonResponse({'status': 'ok'})
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'status': 'ok'})

@csrf_exempt
def telegram_callback(request):
    if request.method == 'POST':
        data = request.POST
        telegram_id = data.get('id')
        first_name = data.get('first_name', '')
        last_name = data.get('last_name', '')
        username = data.get('username', '')
        photo_url = data.get('photo_url', '')

        try:
            # Try to get user by telegram_id
            user = CustomUser.objects.get(telegram_id=telegram_id)
            
            # Update user data if it's changed
            update_fields = []
            if user.first_name != first_name:
                user.first_name = first_name
                update_fields.append('first_name')
            if user.last_name != last_name:
                user.last_name = last_name
                update_fields.append('last_name')
            if user.telegram_username != username:
                user.telegram_username = username
                update_fields.append('telegram_username')
            
            if update_fields:
                user.save(update_fields=update_fields)
                
        except CustomUser.DoesNotExist:
            # Create new user if not exists
            user = CustomUser.objects.create_user(
                phone_number=f'tg_{telegram_id}',  # Temporary phone number
                first_name=first_name,
                last_name=last_name,
                telegram_id=telegram_id,
                telegram_username=username,
                is_verified=True
            )

        # Log the user in
        auth_login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        
        return redirect('dashboard')
    return HttpResponse('Invalid request', status=400)

@method_decorator(login_required, name='dispatch')
class DashboardView(TemplateView):
    template_name = 'index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        # Get user's full name or Telegram username
        full_name = f"{user.first_name or ''} {user.last_name or ''}".strip()
        if not full_name and user.telegram_username:
            full_name = f"@{user.telegram_username}"
        elif not full_name:
            full_name = "Пользователь"
            
        context['user'] = {
            'full_name': full_name,
            'telegram_username': user.telegram_username,
            'role': user.get_role_display(),
            'is_authenticated': user.is_authenticated
        }
        return context

from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
def login_view(request):
    # If user is already authenticated, redirect to home
    if request.user.is_authenticated:
        return redirect('home')
        
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        user = authenticate(request, phone_number=phone_number, password=password)
        
        if user is not None:
            auth_login(request, user)
            # Redirect to 'home' URL name which is defined in config/urls.py
            return redirect('home')
        else:
            messages.error(request, 'Неверный телефон или пароль')
    
    return render(request, 'login.html')

def logout_view(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('home')

# In authentication/views.py
from django.conf import settings
from django.shortcuts import redirect

def telegram_login(request):
    if not hasattr(settings, 'TELEGRAM_BOT_ID') or not settings.TELEGRAM_BOT_ID:
        messages.error(request, 'Telegram bot is not configured. Please contact the administrator.')
        return redirect('login')
        
    telegram_auth_url = (
        f"https://oauth.telegram.org/auth?"
        f"bot_id={settings.TELEGRAM_BOT_ID}&"
        f"origin={request.scheme}://{request.get_host()}&"
        f"request_access=write&"
        f"return_to={request.scheme}://{request.get_host()}/auth/telegram/callback/"
    )
    return redirect(telegram_auth_url)

def telegram_callback(request):
    # Get the auth data from Telegram
    auth_data = request.GET.dict()
    
    # Verify the data (you should add more validation here)
    if 'hash' not in auth_data:
        return redirect('login')
    
    # Here you would typically:
    # 1. Verify the auth_data is valid using the bot token
    # 2. Get or create a user based on the Telegram ID
    # 3. Log the user in
    
    # For now, let's just show the auth data
    return JsonResponse(auth_data)
