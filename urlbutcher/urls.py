from django.urls import path, re_path, include

from . import views



urlpatterns = [
    re_path(r'^$|home/', views.home, name='home'),
    path('slug/', include([
        path('new', views.create_short_slug, name='create_short_slug'),
        path('funny', views.create_funny_slug, name='create_funny_slug'),
        path('chuck', views.create_chuck_norris_slug, name='create_chuck_slug'),
        path('reset_history', views.reset_cookie_last_slugs, name='reset_cookie_last_slugs')
    ])),
    path('<slug:slug_id>/', views.redirect_slug),
]
