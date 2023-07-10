from django import forms
from account.models import Userable, Applicant, Employer
from util.models import Interest
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class ApplicantCreateForm(UserCreationForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta(UserCreationForm.Meta):
        model = Applicant
        fields = ['email', 'username', 'password1', 'password2',
                  'interests', 'nickname', 'age', 'gender',
                  'school', 'career']

class EmployerCreateForm(UserCreationForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta(UserCreationForm.Meta):
        model = Employer
        fields = ['email', 'username', 'password1', 'password2',
                  'interests', 'company']

class ApplicantUpdateForm(UserChangeForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta(UserChangeForm.Meta):
        model = Applicant
        fields = ['nickname', 'age', 'gender', 'school', 'career', 'interests']

class EmployerUpdateForm(UserChangeForm):
    interests = forms.ModelMultipleChoiceField(
        queryset=Interest.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta(UserChangeForm.Meta):
        model = Employer
        fields = ['company', 'interests']
