from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework.routers import SimpleRouter
from api import views

router = SimpleRouter()
router.register('posts', views.PostViewSet)

urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/api-token-auth/', obtain_auth_token),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
]
