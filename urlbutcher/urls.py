from django.urls import path, re_path
from . import views



urlpatterns = [
    re_path(r'^$|home/', views.home, name='home'),
    path('slug/new/', views.create_short_slug, name='create_short_slug'),
    path('slug/funny/', views.create_funny_slug, name='create_funny_slug'),
    path('slug/chuck/', views.create_chuck_norris_slug, name='create_chuck_slug'),
    path('<slug:slug_id>/', views.redirect_slug),
]
