import os
import csv, codecs
import cv2, face_recognition
import numpy as np
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.db.models.query import QuerySet
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.generic import (View, ListView, FormView, 
                                  UpdateView, DeleteView, DetailView)
from django.shortcuts import render, redirect

from face_recognition.face_recognition_cli import image_files_in_folder


from accounts.forms import UpdateUserForm
from accounts.models import User
from institutions.models import InstitutionProfile, InstitutionUser
from .decorators import profile_exists
from . forms import InstitutionUserForm, FillFormDes, UpdateAccusedStatusForm, ApplicantsNameFile, AccusedImageFile
from . models import FillFormModel

# from .compare.compare_face import CompareImage

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

                students = FillFormModel.objects.filter(institution_id = user_profile.institution_id)

                institution_user = InstitutionUser.objects.filter(institution_id = user_profile.institution_id)
                
                return render(request, "malpractice_tracking/dashboard.html", {'user_institution':user_institution, 'students':len(students), 'institution_user':len(institution_user)})
            except InstitutionProfile.DoesNotExist: 
                return render(request, "malpractice_tracking/dashboard.html", {'mssg':'Kindly contact the central admin to update your profile'})
        else:
            user_profile = InstitutionUser.objects.get(user_id=request.user.user_id)
            students = FillFormModel.objects.filter(institution_id = user_profile.institution_id, posted_by = request.user)
            overall_students = FillFormModel.objects.filter(institution_id = user_profile.institution_id)
            return render(request, "malpractice_tracking/dashboard.html", {'students':len(students), 'overall_students':len(overall_students)})


        return render(request, "malpractice_tracking/dashboard.html")

@method_decorator(profile_exists, name="get")
class ManageUsers(LoginRequiredMixin, ListView, FormView):
    template_name = "malpractice_tracking/manage_users.html"
    def get(self, request):
        form = InstitutionUserForm()
        # user_detail = InstitutionUser.objects.get(user_id = pk)
        # user_form = UpdateUserForm(request, instance=user_detail)
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
            messages.error(request, f"An error occurred: {form.errors.as_ul()}")

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
    second_form = AccusedImageFile

    def get(self, request):
        form = self.form_class()
        image_form = self.second_form()
        return render(request, self.template_name, {'form':form, 'image_form':image_form, 'object_list':super().get_queryset()})

    def post(self, request):

        form = self.form_class(request.POST, request.FILES)
        image_form = self.second_form(request.POST, request.FILES)

        print(f"request file: {request.FILES}")
        print(f"request POST: {request.POST}")

        custom_query = []
        if 'name_btn' in request.POST and 'name_file' in request.FILES:
            if form.is_valid():
                csv_obj = csv.reader(codecs.iterdecode(request.FILES['file'], 'utf-8'))

                for f in csv_obj:
                    print(f"f: {f[0]}")
                    data_list = FillFormModel.objects.filter(name__icontains=f[0])
                    print(f"data_list: {data_list}")

                    if data_list:
                        for data in data_list:
                            if not data in custom_query:
                                custom_query.append(data)
                
                print(f"cust: {custom_query}")
            
            else:
                messages.warning(request, f"Error in file: {form.errors.as_text()}")
                return render(request, self.template_name, {'form':form, 'image_form':image_form, 'object_list':super().get_queryset()})
        
        if 'image_btn' in request.POST and 'image_file' in request.FILES:
            if image_form.is_valid():
                # known_accused_face_encodings = []
                # known_accused_face_names = []

                image_file = request.FILES['image_file']
                # image_file = request.FILES.getlist('image_file')

                # load reference image from database
                # accusedProfile = FillFormModel.objects.all()
                # for profile in accusedProfile:
                #     accused = profile.image
                #     image_of_accused = face_recognition.load_image_file(f'media/{accused}')
                #     if len(image_of_accused) > 0:
                #         accused_face_encoding = face_recognition.face_encodings(image_of_accused)[0]
                #         known_accused_face_encodings.append(accused_face_encoding)
                #         known_accused_face_names.append(f'{image_of_accused}'[:-4])
                #     else:
                #         print('Face Not Detected')

                # read the uploaded file and encode the face
               
                image = face_recognition.load_image_file(image_file)
                uploaded_face_encodings = face_recognition.face_encodings(image)

                if len(uploaded_face_encodings) > 0:
                    for profile in FillFormModel.objects.all():
                        profile_image = face_recognition.load_image_file(profile.image.path)
                        profile_image_encodings = face_recognition.face_encodings(profile_image)

                        if len(profile_image_encodings) > 0:
                            profile_image_encoding = profile_image_encodings[0]

                            is_same = face_recognition.compare_faces([profile_image_encoding], uploaded_face_encodings[0])[0]

                            if is_same:
                                # find image distance
                                distance = face_recognition.face_distance([profile_image_encoding], uploaded_face_encodings[0])

                                best_image = np.argmin(distance)
                                # print(distance[best_image])
                                # messages.success(request, f"Best Image: {distance[best_image]}")

                                if distance[best_image] < 0.6:
                                    result = f"Face Found for {profile.name}"
                                    # messages.warning(request, result) 
                                    # messages.success(request, f"{best_image}") 

                                    profile = FillFormModel.objects.get(name=profile.name)
                                    custom_query.append(profile)
                                else:
                                    messages.warning(request, "No close image found") 

                            else:
                                result = ''
                                # messages.warning(request, f"No face found for {profile.name}")
                                print(f"No face found for {profile.name}")
                        else:
                            messages.warning(request, f"No face found in {profile.name} image")

                else:
                    result = "No Face Detected"
                    messages.warning(request, result)
 
                
                return render(request, self.template_name, {'result':result, 'form':form, 'image_form':image_form,'object_list':custom_query})
            
                    
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
    


