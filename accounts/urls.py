from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path, include
from accounts.views import AccountRegisterView, AccountProfileView, RecommendationDetail, AccountLogoutView

app_name = 'accounts'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('register/', AccountRegisterView.as_view(), name='register'),
    path('logout/', AccountLogoutView.as_view(), name='logout'),
    path('profile/', AccountProfileView.as_view(), name='profile') ,
    path('recommendation/<int:pk>', RecommendationDetail.as_view(), name='recommendation'),
]
