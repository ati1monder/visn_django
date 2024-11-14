from django.urls import path
from .modules import *

urlpatterns = [
    path('', AdminIndexView.as_view(), name='admin_index'),
    path('login/', Login.as_view(), name='config_login'),
    path('users/', Users.as_view(), name='users'),
    path('users/<int:id>/', User_Details.as_view(), name='user')
]