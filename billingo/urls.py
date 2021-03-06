"""billingo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import path, include
from django.views.generic.base import TemplateView

from django.conf import settings
from django.conf.urls.static import static
from organisations.views import overview, impressum
from users.views import register, login

urlpatterns = [
    path('', overview, name='home'),#TemplateView.as_view(template_name='./main/index.html'), name='home'),
    path('users/', include('users.urls')),
    path('users/', include('django.contrib.auth.urls')),
    path('registrieren/', register, name='register'),
    path('login/', login, name='login'),
    path('impressum/',impressum, name='impressum'),
    path('admin/', admin.site.urls),
    path('aerzte/', include('recipients.urls')),
    path('rechnungen/',include('invoices.urls')),
    path('anforderungen/',include('submissions.urls')),
    path('organisationen', include('organisations.urls')),
    path('ueberblick/', overview, name='overview'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
