from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from institutions.models import InstitutionProfile, InstitutionUser, Department

from .models import User


class LoginForm(AuthenticationForm):
    username = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'id': 'exampleInputEmail1','class':'form-control form-control-lg', 'placeholder':'Email', 'autofocus': 'true'}))
    password = forms.CharField(max_length=30, required=True, widget=forms.PasswordInput(attrs={'id':'exampleInputPassword1','class':'form-control form-control-lg', 'placeholder':'Password'}))

class UpdateUserForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'id':'name','class':'form-control', 'placeholder':'Enter User Full Name'}))
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label='Select Department', required=True,
                                        widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = InstitutionUser
        fields = [
            'name', 'department'
        ]

    def __init__(self, *args, **kwargs):
        super(UpdateUserForm, self).__init__(*args, **kwargs)

        self.fields['name'] = "hello"
        self.fields['department'].queryset = Department.objects.filter(dept_name = 'Computer Science')
        return
    

class InstitutionProfileForm(forms.ModelForm):
    
    name = forms.CharField(required=False, widget=forms.TextInput(attrs={'id':'name','class':'form-control', 'placeholder':'Enter User Full Name', 'disabled': True}))
    picture = forms.ImageField(required=True, widget=forms.FileInput(attrs={'id':'image', 'name':"picture", 'class':'form-control'}))

    class Meta:
        model = InstitutionProfile
        fields = [
            'name',
            'picture'
        ]

class InstitutionProfileUpdateForm(forms.ModelForm):
    
    # name = forms.CharField(required=False, widget=forms.TextInput(attrs={'id':'name','class':'form-control', 'placeholder':'Enter User Full Name', 'disabled': True}))
    picture = forms.ImageField(required=True, widget=forms.FileInput(attrs={'id':'image', 'name':"picture", 'class':'form-control'}))

    class Meta:
        model = InstitutionProfile
        fields = [
            'picture'
        ]

class InstitutionUserForm(forms.ModelForm):

    picture = forms.ImageField(required=True, widget=forms.FileInput(attrs={'id':'image', 'class':'form-control'}))
    # department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label='Select Department', required=True,
    #                                     widget=forms.Select(attrs={'class':'form-control'}))
    
    class Meta:
        model = InstitutionUser
        fields = [
            'picture',
        ]

class ChangePasswordForm(PasswordChangeForm):

    # old_password = forms.CharField(
    #                                widget=forms.TextInput(
    #                                    attrs={'id':'name',
    #                                           'class':'form-control', 
    #                                           'name': 'old_password',
    #                                           'type': 'password',
    #                                           'placeholder':'Enter your current password'}))
    
    # new_password1 = forms.CharField(
    #                                widget=forms.TextInput(
    #                                    attrs={'id':'name',
    #                                           'class':'form-control', 
    #                                           'name': 'new_password',
    #                                           'type': 'password',
    #                                           'placeholder':'Enter your new password'}))
    
    # new_password2 = forms.CharField(
    #                                widget=forms.TextInput(
    #                                    attrs={'id':'name',
    #                                           'class':'form-control',
    #                                           'name': 'confirm_password',
    #                                           'type': 'password',
    #                                           'placeholder':'Confirm password'}))
    
    # password = forms.CharField(required=False, 
    #                                widget=forms.TextInput(
    #                                    attrs={'id':'name',
    #                                           'class':'form-control',
    #                                           'name': 'confirm_password',
    #                                           'type': 'password',
                                              
    #                                           'placeholder':'password'}))
    
        # class Meta:
        #     model = User
        #     fields = [
        #         'password'
        #     ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].widget= forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Old Password'})
        self.fields["new_password1"].widget = forms.PasswordInput(attrs={"class": "form-control", 'placeholder':'New Password'})
        self.fields["new_password2"].widget = forms.PasswordInput(attrs={"class": "form-control", 'placeholder':'Confirm password'})

    # def clean_confirm_password(self):
    #     new_password = self.cleaned_data.get('new_password')
    #     confirm_password = self.cleaned_data.get('confirm_password')

    #     if new_password != confirm_password:
    #         raise forms.ValidationError("new password and confirm password doesn't match")
        
    #     if len(new_password) < 8:
    #         raise forms.ValidationError("Password should not be less than 8 characters")
        
    #     return confirm_password
    
    # def save(self, commit=True):
    #     user = super().save(commit=False)
    #     user.set_password(self.cleaned_data.get('new_password'))

    #     if commit:
    #         user.save()

    #     return user
    
# class ChangePasswordForm(forms.ModelForm):

#     old_password = forms.CharField(
#                                    widget=forms.TextInput(
#                                        attrs={'id':'name',
#                                               'class':'form-control', 
#                                               'name': 'old_password',
#                                               'type': 'password',
#                                               'placeholder':'Enter your current password'}))
    
#     new_password = forms.CharField(
#                                    widget=forms.TextInput(
#                                        attrs={'id':'name',
#                                               'class':'form-control', 
#                                               'name': 'new_password',
#                                               'type': 'password',
#                                               'placeholder':'Enter your new password'}))
    
#     confirm_password = forms.CharField(
#                                    widget=forms.TextInput(
#                                        attrs={'id':'name',
#                                               'class':'form-control',
#                                               'name': 'confirm_password',
#                                               'type': 'password',
#                                               'placeholder':'Confirm password'}))
    
#     password = forms.CharField(required=False, 
#                                    widget=forms.TextInput(
#                                        attrs={'id':'name',
#                                               'class':'form-control',
#                                               'name': 'confirm_password',
#                                               'type': 'password',
                                              
#                                               'placeholder':'password'}))
    
#     class Meta:
#         model = User
#         fields = [
#             'password'
#         ]

#     def clean_confirm_password(self):
#         new_password = self.cleaned_data.get('new_password')
#         confirm_password = self.cleaned_data.get('confirm_password')

#         if new_password != confirm_password:
#             raise forms.ValidationError("new password and confirm password doesn't match")
        
#         if len(new_password) < 8:
#             raise forms.ValidationError("Password should not be less than 8 characters")
        
#         return confirm_password
    
#     def save(self, commit=True):
#         user = super().save(commit=False)
#         user.set_password(self.cleaned_data.get('new_password'))

#         if commit:
#             user.save()

#         return user
    