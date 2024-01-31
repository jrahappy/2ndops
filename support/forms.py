from django import forms
from .models import Article, Manual, Product, Photo


class ArticleForm(forms.ModelForm):
    manual_pk = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    user = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Article
        fields = [
            "subject",
            "sub_text",
            "description",
            "product_name",
            "manual_pk",  # Include this if you want to save manual_pk in your model
            "ordery",
            "orderx",
        ]


class ArticleDeleteForm(forms.ModelForm):
    manual_pk = forms.IntegerField(widget=forms.HiddenInput(), required=False)
    user = forms.CharField(widget=forms.HiddenInput(), required=False)
    available = forms.BooleanField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = Article
        fields = [
            "subject",
            "sub_text",
            "description",
            "product_name",
            "manual_pk",  # Include this if you want to save manual_pk in your model
            "available",
        ]


class TableOfContentForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = ["subject", "sub_text", "ordery", "orderx"]
        widgets = {
            "subject": forms.TextInput(attrs={"class": "form-control"}),
            "sub_text": forms.TextInput(attrs={"class": "form-control"}),
            "ordery": forms.NumberInput(attrs={"class": "form-control"}),
            "orderx": forms.NumberInput(attrs={"class": "form-control"}),
        }


class ManualForm(forms.ModelForm):
    class Meta:
        model = Manual
        fields = ["title", "product_name", "description", "pdf_file", "available"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.TextInput(attrs={"class": "form-control"}),
            "pdf_file": forms.FileInput(attrs={"class": "form-control"}),
            "available": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ["name", "category", "description", "available"]


class PhotoForm(forms.ModelForm):
    class Meta:
        model = Photo
        fields = ["image", "name", "tags"]
        widgets = {
            "image": forms.FileInput(attrs={"class": "form-control", "multiple": ""}),
            "name": forms.TextInput(attrs={"class": "form-control"}),
            "tags": forms.TextInput(attrs={"class": "form-control"}),
        }
