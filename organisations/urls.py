from django.urls import include, re_path, path
from .views import *
from . import views


app_name = 'organisations'

urlpatterns = [
    path('feedback/', index, name='feedback_index'),
    path('feedback/geben', create, name='feedback_create'),
    path('feedback/change=<int:pk>', change_status, name='feedback_change_status'),
    path('', overview, name='news_index'),
]