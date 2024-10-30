from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

urlpatterns = [
    path('users/register/', view=views.UserView.as_view(), name='user-register'),
    path('users/all/', views.UserListView.as_view()),
    path('users/login/', views.LoginView.as_view(), name='user-login'),
    path('users/logout/', views.LogoutView.as_view(), name='user-logout'),
    path('users/token-balance/', views.TokenBalanceView.as_view(), name='token-balance'),
    path('chats/', views.ChatView.as_view(), name='chat'),
   
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh')
]
