from django.urls import path
from .views import log_in, sign_up, test_token, log_out

urlpatterns = [

    path('login', log_in),
    path('signup', sign_up),
    path('test_token', test_token),
    path('logout', log_out),
    
   
]