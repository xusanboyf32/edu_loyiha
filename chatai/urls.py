from django.urls import path
from . import views

app_name = 'chatai'

urlpatterns = [
    path('', views.chat_page, name='chat_page'),
    path('math/', views.math_chat_page, name='math_chat_page'),
    path('api/', views.chat_api, name='chat_api'),
    path('math/api/', views.math_chat_api, name='math_chat_api'),
    path('history/<str:session_id>/', views.get_history, name='get_history'),
    path('clear/<str:session_id>/', views.clear_history, name='clear_history'),
    path('widget/', views.chat_widget, name='chat_widget'),
]
