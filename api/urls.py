from django.urls import path, include

from . import views



app_name = 'api'

urlpatterns = [
    path('', views.SlugList.as_view(), name='slug_list')
]



# make in api.models with inherting imported Url model
# class UrlManager (models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(user_token=self.token)
