from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth.models import User
from django import forms
from django.core.exceptions import ValidationError

from Taster.models import Country
from Users.models import CustomUser
from django.forms import ModelForm


class RegisterUserForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'class': 'input', }))
    country = forms.ModelChoiceField(queryset=Country.objects.all(), to_field_name='alpha2_code',
                                     widget=forms.HiddenInput())

    class Meta:
        model = CustomUser
        fields = ("email", "username", "password1", "password2", "country")

    def save(self, commit=True):
        user = super(RegisterUserForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        user.country = self.cleaned_data['country']
        if commit:
            user.save()
        return user


class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = CustomUser
        fields = ("old_password", "new_password1", "new_password2")


class EditUserForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ("email", "username")


