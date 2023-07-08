import uuid
from django.db import models
from institutions.models import Department, Session, InstitutionProfile, InstitutionUser
from datetime import date

from accounts.models import User
# Create your models here.
def get_current_year():
    return date.today().year

class FillFormModel(models.Model):
    form_id = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False, unique=True)
    name = models.CharField(max_length=100)
    date = models.DateTimeField(auto_now_add=True)
    registration_no = models.CharField(max_length=50, unique=True)
    posted_by = models.ForeignKey(to=User, on_delete=models.CASCADE)
    institution_id = models.ForeignKey(to=InstitutionProfile, on_delete=models.CASCADE)
    department = models.ForeignKey(to=Department, on_delete=models.SET_NULL, null=True, blank=True)
    session = models.ForeignKey(to=Session, on_delete=models.SET_DEFAULT, default=get_current_year)
    image = models.ImageField(upload_to="img/accused/")
    description = models.CharField(max_length=1000)
    status = models.CharField(max_length=20, choices=[('absolved', 'absolved'),('accused', 'accused'), ('neutral', 'neutral')])

    class Meta:
        verbose_name_plural = "Fill Form"

    def __str__(self) -> str:
        return f"{self.name} from {self.institution_id.name}"