from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("listing/<int:listing_id>/", views.listing, name="listing"),
    path("listing/<int:listing_id>/close/", views.close_listing, name="close_listing"),
    path("listing/<int:listing_id>/comment/", views.comment_listing, name="comment_listing"),
    path("listing/<int:listing_id>/watchlist/<str:action>/", views.watchlist_listing, name="watchlist_listing"),
    path("create/", views.create_listing, name="create_listing"),
    path("watchlist/", views.watchlist, name="watchlist"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register")
]
