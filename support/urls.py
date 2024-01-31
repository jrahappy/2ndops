from django.urls import reverse, path
from . import views

app_name = "support"
urlpatterns = [
    path("", views.home, name="home"),
    path("manual/<int:manual_pk>/detail", views.manual_detail, name="manual-detail"),
    path("manual/<int:manual_pk>/article/>", views.article_list, name="article-list"),
    path(
        "manual/<int:manual_pk>/article/create/",
        views.article_create,
        name="article-create",
    ),
    path(
        "manual/<int:manual_pk>/article/<int:article_pk>/detail",
        views.article_detail,
        name="article-detail",
    ),
    path(
        "manual/<int:manual_pk>/article/<int:article_pk>/update",
        views.article_update,
        name="article-update",
    ),
    path(
        "manual/<int:manual_pk>/article/<int:article_pk>/delete",
        views.article_delete,
        name="article-delete",
    ),
    path(
        "manual/<int:manual_pk>/artticle/<int:article_pk>/create-btw/<int:article_ordery>/<int:article_orderx>",
        views.manual_create_btw,
        name="article-create-btw",
    ),
    path("manual/<int:manual_pk>/reorder", views.manual_reorder, name="manual-reorder"),
    path("manual/<int:manual_pk>/update", views.manual_update, name="manual-update"),
    # photo
    path("photo/create/", views.photo_create, name="photo-create"),
    path("photo/<int:pk>/update", views.photo_update, name="photo-update"),
    path("photo/<int:pk>/delete", views.photo_delete, name="photo-delete"),
    path("photo/<int:pk>/", views.photo_detail, name="photo-detail"),
    path("photo/", views.photo_list, name="photo-list"),
]
