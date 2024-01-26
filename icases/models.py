from django.db import models
from django.urls import reverse
from accounts.models import CustomUser


def upload_to_instance_folder(instance, filename):
    return "reports/{0}/{1}".format(instance.id, filename)


class ICase(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    category = models.CharField(
        choices=[("Normal", "Normal"), ("Big", "Big")], max_length=100, default="Normal"
    )
    target_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    name = models.CharField(max_length=100)
    description = models.TextField()
    report = models.FileField(
        upload_to=upload_to_instance_folder, null=True, blank=True
    )
    status = models.CharField(
        choices=[
            ("Draft", "Draft"),
            ("Processing", "Processing"),
            ("Closed", "Closed"),
        ],
        max_length=100,
        default="Draft",
    )
    tags = models.CharField(max_length=100, default="", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    case_start = models.DateTimeField(null=True, blank=True)
    case_end = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return "{0} - {1}".format(self.user, self.name)

    class Meta:
        ordering = ["-created_at"]

    def get_absolute_url(self):
        return reverse("dashboard:icase-detail", kwargs={"pk": self.pk})


class ICaseComment(models.Model):
    icase = models.ForeignKey(ICase, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    terms = models.IntegerField()
    visits = models.IntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{0} - {1}".format(self.user, self.cost)

    class Meta:
        ordering = ["created_at"]
