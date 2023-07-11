import csv, io
from django import forms
from institutions.models import InstitutionUser, Department, Session
from malpractice_tracking.models import FillFormModel

class InstitutionUserForm(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'id':'name','class':'form-control', 'placeholder':'Enter User Full Name'}))
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'id': 'email', 'class': 'form-control', 'placeholder':'Enter User Email Address'}))
    picture = forms.ImageField(required=False, widget=forms.FileInput(attrs={'id':'image', 'class':'form-control'}))
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label='Select Department', required=True,
                                        widget=forms.Select(attrs={'class':'form-control'}))
    class Meta:
        model = InstitutionUser
        fields = [
            'name', 'email', 'picture', 'department'
        ]

class FillFormDes(forms.ModelForm):
    name = forms.CharField(required=True, widget=forms.TextInput(attrs={'id':'name','class':'form-control', 'placeholder':'Enter Student Full Name(start with first name)'}))
    registration_no = forms.CharField(required=True, widget=forms.TextInput(attrs={'id': 'reg', 'class': 'form-control', 'placeholder':'Enter Registration no(in full)'}))
    image = forms.ImageField(required=True, widget=forms.FileInput(attrs={'id':'image', 'class':'form-control'}))
    
    department = forms.ModelChoiceField(queryset=Department.objects.all(), empty_label='Select Department', required=True,
                                        widget=forms.Select(attrs={'class':'form-control'}))
    session = forms.ModelChoiceField(required=False, queryset=Session.objects.all(), empty_label='Select Session',
                                        widget=forms.Select(attrs={'class':'form-control'}))
    
    description = forms.CharField(widget=forms.Textarea(attrs={'id': 'note', 'class': 'form-control', 'placeholder':'Additional Note'}))
    
    class Meta:
         model = FillFormModel
         fields = [
            'name',
            'registration_no',
            'department',
            'session',
            'image',
            'description'
         ]



class UpdateAccusedStatusForm(forms.ModelForm):

    status_choice = [('absolved', 'absolved'),
                     ('accused', 'accused'),
                     ('neutral', 'neutral')]

    image = forms.ImageField(required=False, widget=forms.FileInput(attrs={'id':'image', 'class':'form-control' }))
    status = forms.ChoiceField(choices=status_choice, required=False, widget=forms.Select(attrs={'class':'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'id': 'note', 'class': 'form-control', 'placeholder':'Additional Note'}))

    class Meta:
        model = FillFormModel
        fields = [
            'image',
            'status',
            'description'
        ]

class FileHandler:
    def __init__(self, obj):
        self.csv_obj = obj
    
    def validate_file(self):
        for row in self.csv_obj:
            if len(row) != 1:raise forms.ValidationError("Invalid File Selected")
            for col in row:
                print(f'col:{col}')
                if len(col) != 1:raise forms.ValidationError("Invalid File Selected")
                if col == '':raise forms.ValidationError('Invalid CSV, Missing DATA!!')
        
class ApplicantsNameFile(forms.Form):
    name_file = forms.FileField(required=False, help_text='Select Applicants File', widget=forms.FileInput(attrs={'name':'name_file', 'class':'form-control', 'accept':'.csv'}))

    def clean_file(self):
        file = io.TextIOWrapper(self.cleaned_data.get('file').file)
        csv_obj = csv.reader(file)

        handler = FileHandler(csv_obj)
        handler.validate_file()

        return file

class AccusedImageFile(forms.Form):
    image_file = forms.FileField(required=False, help_text='Select Individual Image', widget=forms.FileInput(attrs={'name':'image_file', 'class':'form-control'}))
    

