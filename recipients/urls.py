from django.urls import include, re_path, path
from .views import *
from . import views


app_name = 'recipients'

urlpatterns = [
    path('', login_required(doctor_index), name='doctor_index'),
    path('erstellen', login_required(doctor_add), name='doctor_create'),
    path('edit=<int:pk>/', login_required(doctor_edit), name='doctor_edit'),
    path('delete=<int:pk>/', login_required(doctor_delete), name='doctor_delete'),
    path('favorite=<int:recipients>/', login_required(doctor_user_favorit), name='doctor_user_favorit'),
    # path('spezifikationen/import/',type_import, name='type_import'),
]