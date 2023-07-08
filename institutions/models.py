import uuid
from django.db import models

# from accounts.models import User

# Create your models here.

class Department(models.Model):
    dept_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    dept_name = models.CharField(max_length=100, unique=True)
    
    def __str__(self):
        return self.dept_name
    
class Session(models.Model):
    session_id = models.UUIDField(default=uuid.uuid4, unique=True, editable=False, primary_key=True)
    session = models.CharField(max_length=10)

    def __str__(self):
        return self.session
    
class InstitutionProfile(models.Model):
    institution_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    admin_id = models.ForeignKey(to="accounts.User", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, null=True, blank=True)
    picture = models.ImageField(upload_to="img/", null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    

class InstitutionUser(models.Model):
    user_id = models.ForeignKey(to="accounts.User", on_delete=models.CASCADE)
    institution_id = models.ForeignKey(to=InstitutionProfile, on_delete=models.CASCADE, null=True, blank=True)
    institution_user_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    name = models.CharField(max_length=100)
    picture = models.ImageField(default="img/default.jpg", null=True, blank=True)
    department = models.ForeignKey(to=Department, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.name
    


