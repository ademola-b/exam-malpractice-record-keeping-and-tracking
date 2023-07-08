# from django.shortcuts import render, redirect
# from django.contrib.auth.mixins import LoginRequiredMixin
# from django.contrib.messages.views import SuccessMessageMixin
# from django.views.generic import View, DeleteView, UpdateView

# from accounts.models import User
# # Create your views here.
# class DeleteUserView(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
#     model = User
#     success_url = redirect('malpractice:manage_users')
#     success_message = "User Account Successfully Deleted"
    
# class UpdateUser(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
#     model = User
#     success_url = redirect('malpractice:manage_users')
#     success_message = "User Account Successfully Updated"