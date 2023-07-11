from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views

from . views import (LoginView, InstitutionProfileView, 
                     DeleteUser, logout_request, ChangePasswordView)

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('logout/', logout_request, name="logout"),
    path('profile/', InstitutionProfileView.as_view(), name="profile"),
    path('delete-user/<str:pk>/', DeleteUser.as_view(), name="delete_user"),
    path('change-password/',ChangePasswordView.as_view(),name='change_password'),
    
]
