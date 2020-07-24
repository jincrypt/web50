from django.urls import path
from django.views.generic.base import RedirectView

from . import views, util

urlpatterns = [
    path("", RedirectView.as_view(url='wiki/')),
    path("wiki/", views.index, name="index"),
    path("wiki/<str:title>/", views.pages, name="pages"),
    path("search/", views.search, name="search"),
    path("new_page/", views.new_page, name="new_page"),
    path("wiki/<str:title>/edit/", views.edit_page, name="edit_page"),
    path("random_page/",views.random_page, name="random_page")

]
