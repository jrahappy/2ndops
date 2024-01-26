from django.urls import path
from .views import ICaseListView, ICaseCreateView, ICaseDetailView

app_name = "dashboard"
urlpatterns = [
    path("", ICaseListView.as_view(), name="icase-list"),
    path("icase/create/", ICaseCreateView.as_view(), name="icase-create"),
    path("icase/<int:pk>/", ICaseDetailView.as_view(), name="icase-detail"),
    # path("icase/<int:pk>/update/", ICaseUpdateView.as_view(), name="icase_update"),
    # path("icase/<int:pk>/delete/", ICaseDeleteView.as_view(), name="icase_delete"),
]
