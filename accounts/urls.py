from django.urls import path
from . views import LoginView, DeleteUser

app_name = 'accounts'
urlpatterns = [
    path('login/', LoginView.as_view(), name="login"),
    path('delete-user/<str:pk>/', DeleteUser.as_view(), name="delete_user"),
    
]
