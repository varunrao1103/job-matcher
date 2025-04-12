from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser
from django import forms
from .models import Job
from .models import Application

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password1', 'password2', 'user_type']

class JobForm(forms.ModelForm):
    class Meta:
        model = Job
        fields = ["title", "description", "requirements"]
    
class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ["cover_letter", "resume"]  # Include resume field

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["resume"].required = True  # Make resume required