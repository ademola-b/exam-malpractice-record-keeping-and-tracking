from typing import Any, Optional
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import views as auth_views
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.views.generic import View, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.urls import reverse_lazy
from django.contrib.auth import update_session_auth_hash
from django.shortcuts import render, redirect
from accounts.models import User
from . forms import (LoginForm, UpdateUserForm, InstitutionProfileForm, 
                     InstitutionProfileUpdateForm, InstitutionUserForm, ChangePasswordForm)

from institutions.models import InstitutionUser, InstitutionProfile

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
            messages.error(request, f"An error occurred: {form.errors.as_text()}")
        
        return render(request, self.template_name, {'form':form})
    

def logout_request(request):
    logout(request)
    return redirect('accounts:login')

class DeleteUser(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = User
    success_url = reverse_lazy("malpractice:manage_users")
    success_message = "User Successfully Deleted"

class UpdateUser(LoginRequiredMixin, SuccessMessageMixin, DeleteView):
    model = InstitutionUser
    form_class = UpdateUserForm
    success_url = reverse_lazy("malpractice:manage_users")
    success_message = "User Successfully Updated"

    def get(self, request, pk, *args, **kwargs):
        user_detail = InstitutionUser.objects.get(user_id = pk)
        form = self.form_class(request, instance=user_detail)
        return render(request, "malpractice_tracking/manage_users.html", {'form':form})


class InstitutionProfileView(LoginRequiredMixin,auth_views.PasswordChangeView, SuccessMessageMixin, UpdateView, ):
    # model = InstitutionProfile
    template_name = "malpractice_auth/profile.html"
    

    def get(self, request):
        form = ChangePasswordForm(request.user)
        try:
            if request.user.is_institution_admin:
                user_id = User.objects.get(user_id = request.user.pk)
                institution_profile = InstitutionProfile.objects.get(admin_id = user_id)
                # get the institution data
                institution_profile = InstitutionProfile.objects.get(institution_id = institution_profile.institution_id)
                print(f"instP: {institution_profile.institution_id}")
                institution_form = InstitutionProfileForm(instance=institution_profile)
                return render(request, self.template_name, {'institution_form':institution_form, 'user_data':institution_profile, 'form':form})     
            else:
                institution_user = InstitutionUser.objects.get(user_id = request.user)
                institution_form = InstitutionUserForm(instance=institution_user)
                return render(request, self.template_name, {'institution_form':institution_form, 'user_data':institution_user, 'form':form})       
        except ObjectDoesNotExist:
            messages.warning(request, "Accound not found")
            return redirect("accounts:profile")
    
    def post(self, request):    
        print(request.POST)
        try:
            if request.user.is_institution_admin:
                user_id = User.objects.get(user_id = request.user.pk)
                institution_profile = InstitutionProfile.objects.get(admin_id = user_id)
                # get the institution data
                institution_profile = InstitutionProfile.objects.get(institution_id = institution_profile.institution_id)
                institution_form = InstitutionProfileUpdateForm(request.POST, request.FILES, instance=institution_profile)
                if 'update_profile' in request.POST:
                    print(f"instPos: {request.POST}")

                    if institution_form.is_valid():
                        if 'picture' in request.POST:
                            messages.warning(request, "No picture was selected")
                        else:
                            messages.success(request, "Account Successfully Updated")
                            institution_form.save()
                    else:
                        messages.warning(request, f"{institution_form.errors.as_text()}")

                    return redirect("accounts:profile")
            else:
                institution_user = InstitutionUser.objects.get(user_id = request.user)
                institution_form = InstitutionUserForm(request.POST, request.FILES, instance=institution_user)
                if 'update_profile' in request.POST:
                    if institution_form.is_valid():
                        # if form.cleaned_data.get('picture'):
                        if 'picture' in request.POST:
                            messages.warning(request, "No picture was selected")
                        else:
                            messages.success(request, "Account Successfully Updated")
                            institution_form.save()
                    else:
                        messages.warning(request, f"{institution_form.errors.as_text()}")

                    return redirect("accounts:profile")            
                
            if 'change_password' in request.POST:
                form = ChangePasswordForm(request, request.POST)
                if form.is_valid():
                    form.save()
                    # Updating the password logs out all other sessions for the user
                    # except the current one.
                    update_session_auth_hash(self.request, form.user)
                    return super().form_valid(form)
                    # return self.form_valid(form)
                else:
                    print("an error")
                    # return self.form_invalid(form)

        except ObjectDoesNotExist:
            messages.warning(request, "Accound not found")
            return redirect("accounts:profile")
        return render(request, self.template_name, {'institution_form':institution_form, 'user_data':institution_profile, 'form':form})
        
        
            
class ChangePasswordView(auth_views.PasswordChangeView):
    form_class = ChangePasswordForm
    success_url = reverse_lazy('accounts:login')
    template_name='malpractice_auth/change-password.html'




