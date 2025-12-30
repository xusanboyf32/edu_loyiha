# authentication/urls.py
from django.urls import path
from .views import (
     CheckAuthView,
    LogoutView, AdminCreateUserView,
    telegram_auth_start, telegram_auth_verify,
    telegram_webhook, telegram_callback
)

urlpatterns = [
    # Kirish uchun
    # path('telegram-login/', TelegramLoginView.as_view(), name='telegram-login'),
    # path('verify-code/', VerifyCodeView.as_view(), name='verify-code'),
    path('check-auth/', CheckAuthView.as_view(), name='check-auth'),
    path('logout/', LogoutView.as_view(), name='logout'),

    # Telegram Auth
    path('telegram/start/', telegram_auth_start, name='telegram_auth_start'),
    path('telegram/verify/', telegram_auth_verify, name='telegram_auth_verify'),
    path('telegram/webhook/', telegram_webhook, name='telegram_webhook'),
    path('telegram/callback/', telegram_callback, name='telegram_callback'),

    # Admin uchun
    path('admin/create-user/', AdminCreateUserView.as_view(), name='admin-create-user'),
]


