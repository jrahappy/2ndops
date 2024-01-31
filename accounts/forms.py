from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Profile
from django.db import transaction

GENDER_CHOICES = [
    ("Male", "Male"),
    ("Female", "Female"),
    ("Other", "Other"),
]


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
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True)
    cellphone = forms.CharField(max_length=100, required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
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
        patient = Profile.objects.create(user=custom_user)
        patient.birth_date = self.cleaned_data.get("birth_date")
        patient.cellphone = self.cleaned_data.get("cellphone")
        patient.gender = self.cleaned_data.get("gender")
        patient.save()
        return custom_user


class DoctorCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    password1 = forms.CharField(widget=forms.PasswordInput, label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput, label="Confirm Password")
    orgarnization = forms.CharField(max_length=100, required=True)
    address = forms.CharField(max_length=100, required=True)
    suite = forms.CharField(max_length=20, required=True)
    city = forms.CharField(max_length=20, required=True)
    state = forms.CharField(max_length=20, required=True)
    zipcode = forms.CharField(max_length=10, required=True)
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    office_email = forms.EmailField(required=True)
    office_phone = forms.CharField(max_length=20, required=True)
    cellphone = forms.CharField(max_length=100, required=True)

    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = (
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "orgarnization",
            "address",
            "suite",
            "city",
            "state",
            "zipcode",
            "office_email",
            "office_phone",
            "cellphone",
        )

    @transaction.atomic
    def save(self):
        custom_user = super().save(commit=False)
        custom_user.email = self.cleaned_data.get("email")
        custom_user.first_name = self.cleaned_data.get("first_name")
        custom_user.last_name = self.cleaned_data.get("last_name")
        custom_user.save()
        doctor = Profile.objects.create(user=custom_user)
        doctor.category = "Doctor"
        doctor.organization = self.cleaned_data.get("orgarnization")
        doctor.address = self.cleaned_data.get("address")
        doctor.suite = self.cleaned_data.get("suite")
        doctor.city = self.cleaned_data.get("city")
        doctor.state = self.cleaned_data.get("state")
        doctor.zipcode = self.cleaned_data.get("zipcode")
        doctor.office_email = self.cleaned_data.get("office_email")
        doctor.office_phone = self.cleaned_data.get("office_phone")
        doctor.cellphone = self.cleaned_data.get("cellphone")
        doctor.save()
        return custom_user


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


class ProfileForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=False
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False)

    class Meta:
        model = Profile
        fields = (
            # "user",
            # "category",
            # "avatar",
            "bio",
            "cellphone",
            "birth_date",
            "gender",
            "address",
            "suite",
            "city",
            "state",
            "zipcode",
        )


class PatientProfileForm(forms.ModelForm):
    birth_date = forms.DateField(
        widget=forms.DateInput(attrs={"type": "date"}), required=False
    )
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=False)

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


class DoctorProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            # "user",
            "category",
            "organization",
            "address",
            "suite",
            "city",
            "state",
            "zipcode",
            "office_email",
            "office_phone",
            "cellphone",
            "bio",
            "avatar",
        )
