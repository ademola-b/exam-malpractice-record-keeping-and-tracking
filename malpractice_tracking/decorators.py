from django.contrib import messages
from django.shortcuts import redirect
from institutions.models import InstitutionProfile

def profile_exists(func):
    def wrapper_func(request, *args, **kwargs):
        try:
            user = request.user
            if user.is_institution_admin:
                InstitutionProfile.objects.get(admin_id=user.user_id)
            return func(request, *args, **kwargs)
        except InstitutionProfile.DoesNotExist:
                messages.warning(request, 'Account has not been updated, Contact the central admin!!')
                return redirect('malpractice:dashboard')
    return wrapper_func

