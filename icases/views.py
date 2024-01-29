from django.shortcuts import render, redirect, reverse
from django.views import View
from django.views.generic import (
    ListView,
    CreateView,
    DetailView,
    UpdateView,
    DeleteView,
)

from .models import ICase, ICaseComment, TreatPlan, TreatPlanDetail
from .forms import ICaseForm, TreatPlanForm
from django.core.paginator import Paginator
from django.contrib.auth.mixins import LoginRequiredMixin


class ICaseListView(LoginRequiredMixin, ListView):
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


class ICaseDetailView(LoginRequiredMixin, DetailView):
    model = ICase
    template_name = "icases/icase_detail.html"
    context_object_name = "icase"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["icase_comments"] = ICaseComment.objects.filter(icase=self.object)
        return context


class ICaseUpdateView(LoginRequiredMixin, UpdateView):
    def get(self, request, pk):
        icase = ICase.objects.get(pk=pk)
        form = ICaseForm(instance=icase)
        return render(request, "icases/icase_edit.html", {"form": form})

    def post(self, request, pk):
        icase = ICase.objects.get(pk=pk)
        form = ICaseForm(request.POST, request.FILES, instance=icase)
        if form.is_valid():
            form.save()
            return redirect("icases:icase-detail", pk=icase.pk)
        return render(request, "icases/icase_edit.html", {"form": form})

    def get_success_url(self):
        return reverse("icases:icase-detail", kwargs={"pk": self.object.pk})


class ICaseDeleteView(LoginRequiredMixin, DeleteView):
    model = ICase
    template_name = "icases/icase_delete.html"
    context_object_name = "icase"

    def get_success_url(self):
        return reverse("icases:icase-list")


class ICaseCreateView(LoginRequiredMixin, View):
    def get(self, request):
        form = ICaseForm()
        return render(request, "icases/icase_create.html", {"form": form})

    def post(self, request):
        form = ICaseForm(request.POST, request.FILES)
        print("form: ", form)
        if form.is_valid():
            icase = form.save(commit=False)
            icase.user = request.user
            print("icase.report: ", icase.report)
            icase.save()
            return redirect("icases:icase-detail", pk=icase.pk)
        return render(request, "icases/icase_create.html", {"form": form})


class TPlanCreateView(CreateView):
    model = TreatPlan
    template_name = "icases/tplan_create.html"
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
