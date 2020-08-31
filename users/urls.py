from django.urls import path
from .views import profile_edit, profile_show

app_name = 'users'

urlpatterns = [
    path('profile/edit/', profile_edit, name='profile_edit'),
    path('profile/show/', profile_show, name='profile_show'),
]