from django.shortcuts import render
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .models import ICase, ICaseComment


class ICaseListView(ListView):
    model = ICase
    template_name = "icases/icase_list.html"
    context_object_name = "icases"
    paginate_by = 10

    def get_queryset(self):
        return ICase.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # context["icase_comments"] = ICaseComment.objects.all()
        return context


class ICaseDetailView(DetailView):
    model = ICase
    template_name = "icases/icase_detail.html"
    context_object_name = "icase"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     # context["icase_comments"] = ICaseComment.objects.all()
    #     return context
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["icase_comments"] = ICaseComment.objects.filter(icase=self.object)
        return context


class ICaseCreateView(CreateView):
    model = ICase
    template_name = "icases/icase_create.html"
    fields = [
        "category",
        "target_cost",
        "name",
        "description",
        "report",
        "status",
        "tags",
    ]

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.status = "Draft"
        form.save()
        return super().form_valid(form)
