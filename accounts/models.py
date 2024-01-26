from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    pass

    def __str__(self):
        return self.email


class Profile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    category = models.CharField(
        choices=[("Patient", "Patient"), ("Doctor", "Doctor"), ("Staff", "Staff")],
        max_length=20,
        null=True,
        blank=True,
        default="Patient",
    )
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    cellphone = models.CharField(max_length=100, null=True, blank=True)
    gender = models.CharField(
        choices=[("Male", "Male"), ("Female", "Female")],
        max_length=10,
        null=True,
        blank=True,
    )
    birth_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return "{0} - {1}".format(self.user, self.category)
