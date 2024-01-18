from django.urls import path, re_path
from .views import *

urlpatterns = [
    path('', Home_No_Auto.as_view(), name='home_no_auto'),
    path('home/<slug:user_id>', Home.as_view(), name='home'),
    path('home/find_message', Find_message.as_view(), name='find_message')
    ]