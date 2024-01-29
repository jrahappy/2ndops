from django import forms
from .models import ICase, ICaseComment, TreatPlan, TreatPlanDetail


class ICaseForm(forms.ModelForm):
    category = forms.ChoiceField(
        choices=ICase.CATEGORY_CHOICES,
        initial="Normal",
        label="Case Category",
        widget=forms.Select(
            attrs={"class": "form-control", "style": "width:200px;margin-bottom:10px"}
        ),
    )
    target_cost = forms.DecimalField(
        max_digits=8,
        decimal_places=2,
        widget=forms.NumberInput(
            attrs={"class": "form-control", "style": "width:200px;margin-bottom:10px"}
        ),
        initial=0.00,
    )
    name = forms.CharField(
        label="Case title",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "style": "margin-bottom:10px"}
        ),
    )
    description = forms.CharField(
        label="Case description",
        widget=forms.Textarea(
            attrs={"class": "form-control", "style": "margin-bottom:10px"}
        ),
    )
    status = forms.ChoiceField(
        choices=ICase.STATUS_CHOICES,
        label="Case status",
        initial="Draft",
        widget=forms.Select(
            attrs={"class": "form-control", "style": "width:200px;margin-bottom:10px"}
        ),
    )
    report = forms.FileField(
        label="File Upload",
        widget=forms.FileInput(
            attrs={
                "class": "form-control",
                "style": "margin-bottom:10px",
                "multiple": False,
            }
        ),
        required=False,
    )
    tags = forms.CharField(
        label="Tags",
        max_length=100,
        widget=forms.TextInput(
            attrs={"class": "form-control", "style": "margin-bottom:10px"}
        ),
        required=False,
    )

    class Meta:
        model = ICase
        fields = [
            "category",
            "target_cost",
            "name",
            "description",
            "status",
            "report",
            "tags",
        ]

    def clean(self):
        cleaned_data = super().clean()
        # category = cleaned_data.get("category")
        target_cost = cleaned_data.get("target_cost")
        status = cleaned_data.get("status")
        report = cleaned_data.get("report")

        if status == "Published" and not report:
            raise forms.ValidationError(
                "You must upload a report if you want to publish this case."
            )

        if status == "Published" and target_cost == 0.00:
            raise forms.ValidationError(
                "You must set a target cost if you want to publish this case."
            )


class TreatPlanForm(forms.ModelForm):
    name = forms.CharField(max_length=100)
    description = forms.CharField(widget=forms.Textarea)
    cost = forms.DecimalField(max_digits=10, decimal_places=2, initial=0.00)
    terms = forms.IntegerField()
    visits = forms.IntegerField()

    class Meta:
        model = TreatPlan
        fields = ["name", "description", "cost", "terms", "visits"]
