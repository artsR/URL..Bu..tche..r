from django.urls import path, include

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from . import views



app_name = 'api'

urlpatterns = [
    path('', views.api_root),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh', TokenRefreshView.as_view(), name='token_refresh'),
    path('slugs/', views.SlugList.as_view(), name='slug_list'),
    path('slugs/<slug:pk>/', views.SlugDetail.as_view(), name='slug_detail'),
    # path('slugs/types', views.SlugTypes, name='slug_types'),
]



# make in api.models with inherting imported Url model
# class UrlManager (models.Manager):
#     def get_queryset(self):
#         return super().get_queryset().filter(user_token=self.token)
