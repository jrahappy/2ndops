from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile
from django.db import transaction


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            "email",
            "username",
        )


class PatientCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")

    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=True
    )
    gender = forms.CharField(max_length=10, required=True)
    cellphone = forms.CharField(max_length=100, required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            "username",
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "gender",
            "birth_date",
            "cellphone",
        )

    @transaction.atomic
    def save(self):
        custom_user = super().save(commit=False)
        custom_user.email = self.cleaned_data.get("email")
        custom_user.first_name = self.cleaned_data.get("first_name")
        custom_user.last_name = self.cleaned_data.get("last_name")
        custom_user.save()
        patient = Profile.objects.create(user=user)
        patient.birth_date = self.cleaned_data.get("birth_date")
        patient.cellphone = self.cleaned_data.get("cellphone")
        patient.gender = self.cleaned_data.get("gender")
        patient.save()


# class CustomerSignUpForm(UserCreationForm):
#     first_name = forms.CharField(required=True)
#     last_name = forms.CharField(required=True)
#     phone_number = forms.CharField(required=True)
#     location = forms.CharField(required=True)

#     class Meta(UserCreationForm.Meta):
#         model = User

#     @transaction.atomic
#     def save(self):
#         user = super().save(commit=False)
#         user.is_customer = True
#         user.first_name = self.cleaned_data.get('first_name')
#         user.last_name = self.cleaned_data.get('last_name')
#         user.save()
#         customer = Customer.objects.create(user=user)
#         customer.phone_number=self.cleaned_data.get('phone_number')
#         customer.location=self.cleaned_data.get('location')
#         customer.save()
#         return user


class CustomUserChangeForm(UserChangeForm):
    password = None
    first_name = forms.CharField(max_length=100, required=False)
    last_name = forms.CharField(max_length=100, required=False)

    class Meta:
        model = CustomUser
        fields = (
            "username",
            "first_name",
            "last_name",
        )


GENDER_CHOICES = [
    ("M", "Male"),
    ("F", "Female"),
    ("O", "Other"),
]


class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=False
    )

    class Meta:
        model = Profile
        fields = (
            # "user",
            "category",
            # "avatar",
            "bio",
            "cellphone",
            "birth_date",
            "gender",
        )
