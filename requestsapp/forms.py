from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import inlineformset_factory

from .models import EligibilityRequest, ClientQuery

class PartnerSignUpForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Used to send you results and notifications.")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")

class PartnerLoginForm(AuthenticationForm):
    pass

ClientQueryFormSet = inlineformset_factory(
    EligibilityRequest,
    ClientQuery,
    fields=("first_name", "middle_name", "last_name", "dob"),
    extra=1,
    can_delete=True,
    widgets={
        "dob": forms.DateInput(attrs={"type": "date"}),
    },
)

ReviewClientQueryFormSet = inlineformset_factory(
    EligibilityRequest,
    ClientQuery,
    fields=("first_name", "middle_name", "last_name", "dob", "eligibility", "reviewer_notes"),
    extra=0,
    can_delete=False,
    widgets={
        "dob": forms.DateInput(attrs={"type": "date"}),
        "reviewer_notes": forms.Textarea(attrs={"rows": 2}),
    },
)
