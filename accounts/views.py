from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views.generic import View, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from accounts.models import User
from . forms import LoginForm

# Create your views here.

class LoginView(View):
    template_name = "malpractice_auth/login.html"

    def get(self, request):
        form = LoginForm()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = LoginForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('malpractice:dashboard')
                else:
                    messages.error(request, "Your account is not active, kindly contact the admin")
            else:
                messages.error(request, "Account not found")
        else:
            messages.error(request, f"An error occurred: {form.errors.as_text}")
        
        return render(request, self.template_name, {'form':form})
    
class DeleteUser(SuccessMessageMixin, DeleteView):
    model = User
    success_url = reverse_lazy("malpractice:manage_users")
    success_message = "User Successfully Deleted"



    
