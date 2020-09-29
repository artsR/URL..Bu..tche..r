from django.urls import path, re_path, include

from . import views



urlpatterns = [
    re_path(r'^$|home/', views.home, name='home'),
    path('slug/', include([
        path('new', views.create_short_slug, name='create_short_slug'),
        path('funny', views.create_funny_slug, name='create_funny_slug'),
        path('chuck', views.create_chuck_norris_slug, name='create_chuck_slug'),
        path('reset_history', views.reset_cookie_last_slugs, name='reset_cookie_last_slugs'),
        path('refresh/<slug:slug_id>/', views.refresh_slug, name='refresh_slug'),
        path('edit/<slug:slug_id>/', views.edit_slug, name='edit_slug'),
        path('delete/<slug:slug_id>/', views.delete_slug, name='delete_slug'),
        path('dashboard', views.dashboard, name='dashboard'),
    ])),
    path('<slug:slug_id>/', views.redirect_slug, name='redirect_slug'),
]
