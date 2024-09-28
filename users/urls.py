from django.urls import path , include
from .views import log_in, sign_up,  log_out, ProfileViewSet
from rest_framework.routers import DefaultRouter


router = DefaultRouter()
router.register(r'profiles', ProfileViewSet, basename='profile')

urlpatterns = [
    path('', include(router.urls)),
    path('login', log_in, name='login'),
    path('signup', sign_up, name='signup'),
    path('logout', log_out, name='logout'),
]