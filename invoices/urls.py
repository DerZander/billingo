from django.contrib.auth.decorators import login_required
from django.urls import include, re_path, path
from .views import *
from . import views


app_name = 'invoices'

urlpatterns = [
    path('', login_required(index), name='invoice_index'),
    path('arzt/<str:recipient>',index, name='invoice_index_doctor'),
    path('status/<str:filter>',index, name='invoice_index_filter'),
    path('bezahlen/<int:pk>/<str:demands>', paid, name='invoice_paid'),
    path('entfernen/<int:pk>', retreat, name='invoice_retreat'),
    path('erstellen', add, name='invoice_create'),
    path('erstellen/recipient=<int:recipient>', add, name='invoice_add'),
    path('edit/<int:pk>', edit, name='invoice_edit'),
    path('delete/<int:pk>', delete, name='invoice_delete'),
]