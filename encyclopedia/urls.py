
from django.urls import path

from . import views

app_name = "wiki"

urlpatterns = [
    path("", views.index, name="index"),
    path("wiki/<str:title>", views.pages, name="pages"),
    path("search/", views.searchpage, name="search"),
    path("new/", views.newentry, name="newentry"),
    path("save/", views.saveentry, name="saveentry"),
    path("edit/", views.editpage, name="edit"),
    path("change/", views.savechanges, name="savechange")
    # path("wiki", views.searchpage, name="search")
]
