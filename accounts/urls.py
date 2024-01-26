from django.urls import path
from . import views


app_name = "accounts"
urlpatterns = [
    path("user_update", views.user_update, name="user-update"),
    path("user_profile", views.user_profile, name="user-profile"),
    path("new_patient", views.new_patient, name="new-patient"),
    # path("icase/create/", ICaseCreateView.as_view(), name="icase-create"),
    # path("icase/<int:pk>/", ICaseDetailView.as_view(), name="icase-detail"),
    # # path("icase/<int:pk>/update/", ICaseUpdateView.as_view(), name="icase_update"),
    # path("icase/<int:pk>/delete/", ICaseDeleteView.as_view(), name="icase_delete"),
]
