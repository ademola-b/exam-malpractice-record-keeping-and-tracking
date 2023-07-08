import csv, codecs
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (View, ListView, FormView, 
                                  UpdateView, DeleteView, DetailView)
from django.shortcuts import render, redirect

from accounts.models import User
from institutions.models import InstitutionProfile, InstitutionUser
from .decorators import profile_exists
from . forms import InstitutionUserForm, FillFormDes, UpdateAccusedStatusForm, ApplicantsNameFile
from . models import FillFormModel

password = "12345678"
# Create your views here.
class LandingView(View):
    def get(self, request):
        return render(request, "malpractice_tracking/landing.html")

class Dashboard(View, LoginRequiredMixin):
    def get(self, request):
        if request.user.is_institution_admin:
            try:
                user_profile = InstitutionProfile.objects.get(admin_id=request.user.user_id)
                user_institution = user_profile.name
                return render(request, "malpractice_tracking/dashboard.html", {'user_institution':user_institution})
            except InstitutionProfile.DoesNotExist: 
                return render(request, "malpractice_tracking/dashboard.html", {'mssg':'Kindly contact the central admin to update your profile'})
        return render(request, "malpractice_tracking/dashboard.html")

@method_decorator(profile_exists, name="get")
class ManageUsers(LoginRequiredMixin, ListView, FormView):
    template_name = "malpractice_tracking/manage_users.html"
    def get(self, request):
        form = InstitutionUserForm()
        institution_profile = InstitutionProfile.objects.get(admin_id=request.user.user_id) 
        institution_users=InstitutionUser.objects.filter(institution_id=institution_profile)
        if institution_users.exists():
            return render(request, self.template_name, {'institution_users':institution_users, 'form':form})
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = InstitutionUserForm(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            user = User.objects.create_user(email=form.cleaned_data['email'], password=password)
            institution_profile = InstitutionProfile.objects.get(admin_id=request.user.user_id)
            print(f"inst: {institution_profile}")
            instance.user_id = user
            instance.institution_id = institution_profile
            instance.save()
            messages.success(request, "User Account Successfully Saved")
            return redirect('malpractice:manage_users')
        else:
            messages.error(request, f"An error occurred: {form.errors.as_text()}")
            return render(request, self.template_name, {'form':form})


@method_decorator(profile_exists, name="get")
class FillForm(LoginRequiredMixin, FormView):
    form_class = FillFormDes
    template_name = "malpractice_tracking/fill-form.html"
    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            user = User.objects.get(user_id = request.user.user_id)
            instance.posted_by = user

            if request.user.is_institution_admin:
                profile = InstitutionProfile.objects.get(admin_id = request.user.user_id)
                instance.institution_id = profile
            else:
                institution_user = InstitutionUser.objects.get(user_id = request.user.user_id)
                instance.institution_id = institution_user.institution_id
            
            instance.status = "accused"
            instance.department = form.cleaned_data['department']
            instance.session = form.cleaned_data['session']

            instance.save()
            messages.success(request, "Student Added to database")
            return redirect('malpractice:fill_form')
        else:
            messages.error(request, f"An error occurred: {form.errors.as_ul}")

        return render(request, self.template_name, {'form':form})

@method_decorator(profile_exists, name="get")    
class AccusedList(SuccessMessageMixin, LoginRequiredMixin, ListView, UpdateView):
    # form_class = UpdateAccusedStatusForm

    def get_initial(self):
        initial = super().get_initial()
        data = self.get_object()
        initial['status'] = data.status
        initial['description'] = data.description
        return initial

    def get(self, request):
        # accused_status = get_object_or_404(FillFormModel, pk)
        # form = UpdateAccusedStatusForm()
        accusedList = FillFormModel.objects.filter(posted_by = request.user)
        if request.user.is_institution_admin:
            institution = InstitutionProfile.objects.get(admin_id = request.user.user_id)
            accusedList = FillFormModel.objects.filter(institution_id = institution)

        if accusedList.exists():
            return render(request, "malpractice_tracking/accused-list.html", {'accusedList':accusedList})
        
        return render(request, "malpractice_tracking/accused-list.html")
    
class UpdateAccusedStatus(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    model = FillFormModel
    form_class = UpdateAccusedStatusForm
    template_name = "utils/update-accused-status.html"
    success_message = "Accused Student Successfully Updated"
    success_url = reverse_lazy("malpractice:accused_list")

    def get_initial(self):
        initial = super().get_initial()
        data = self.get_object()
        initial['status'] = data.status
        initial['description'] = data.description
        return initial

class DeleteAccused(SuccessMessageMixin, LoginRequiredMixin, DeleteView):
    model = FillFormModel
    # template_name = "malpractice_tracking/update-accused-status.html"
    success_message = "Accused Successfully Deleted"
    success_url = reverse_lazy("malpractice:accused_list")

@method_decorator(profile_exists, name="get")
class TrackAccusedView(ListView, FormView):
    model = FillFormModel
    template_name = "malpractice_tracking/track-accused.html"
    # context_object_name = "accused_list"
    form_class = ApplicantsNameFile

    def post(self, request):
        form = self.form_class(request.POST, request.FILES)

        custom_query = []
        if form.is_valid():
            csv_obj = csv.reader(codecs.iterdecode(request.FILES['file'], 'utf-8'))

            for f in csv_obj:
                print(f"f: {f[0]}")
                data_list = FillFormModel.objects.filter(name__icontains=f[0])
                print(f"data_list: {data_list}")

                if data_list:
                    for data in data_list:
                        if not d in custom_query:
                            custom_query.append(data)
            
            print(f"cust: {custom_query}")
        
        else:
            messages.warning(request, f"Error in file: {form.errors.as_text()}")
            return render(request, self.template_name, {'form':form, 'object_list':super().get_queryset()})
        
        return render(request, self.template_name, {'form':form, 'object_list':custom_query})
        
class AccusedDetailView(DetailView):
    model = FillFormModel
    template_name = "malpractice_tracking/accused-detail.html"


class SearchResult(ListView):
    model = FillFormModel
    template_name = "malpractice_tracking/search.html"

    def get_queryset(self):
        qs = FillFormModel.objects.none()

        if hasattr(self, 'modified_query'):
            qs = self.modified_query
        return qs
    
    def post(self, request, *args, **kwargs):
        query = self.request.POST['query']

        self.modified_query = self.get_query(query)
        return self.get(request, *args, **kwargs)

    def get_query(self, query):
        return FillFormModel.objects.filter(name__icontains=query) | FillFormModel.objects.filter(institution_id__name__icontains=query)