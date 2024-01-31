from django.db import models
from django.urls import reverse
from accounts.models import CustomUser


def upload_location(instance, filename):
    return "files/support/%s/%s" % (instance.id, filename)


class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name


class Manual(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, blank=True, null=True
    )
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=250, null=True, blank=True)
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    pdf_file = models.FileField(upload_to=upload_location, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.title


# class ManualTableOfContent(models.Model):
#     manual_title = models.ForeignKey(Manual, on_delete=models.CASCADE)
#     subject = models.CharField(max_length=100)
#     sub_text = models.CharField(max_length=100)
#     ordery = models.IntegerField()
#     orderx = models.IntegerField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     available = models.BooleanField(default=True)

#     def __str__(self):
#         return self.subject


class Article(models.Model):
    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, blank=True, null=True
    )
    subject = models.CharField(max_length=100)
    sub_text = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField()
    ordery = models.IntegerField(default=0)
    orderx = models.IntegerField(default=0)
    product_name = models.ForeignKey(Product, on_delete=models.CASCADE)
    manual_name = models.ForeignKey(Manual, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.subject

    def get_absolute_url(self):
        return reverse("support:article-detail", kwargs={"pk": self.pk})


def photo_location(instance, filename):
    return "media/%s/%s" % (instance.id, filename)


class Photo(models.Model):
    class Meta:
        verbose_name = "Photo"
        verbose_name_plural = "Photos"

    user = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, blank=True, null=True
    )
    image = models.ImageField(null=False, blank=False)
    name = models.CharField(max_length=255, blank=True)
    tags = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.description
