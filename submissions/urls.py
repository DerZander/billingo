from django.urls import include, re_path, path
from .views import *
from . import views


app_name = 'submissions'

urlpatterns = [
    path('', index, name='submissions_index'),
    path('detail/<int:submission_id>',detail, name='submissions_detail'),
    path('senden/<int:submission_id>',send, name='submissions_request'),
]