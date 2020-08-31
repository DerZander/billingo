from django.contrib import admin
from .models import *

admin.site.register(Recipient)
admin.site.register(RecipientType)
admin.site.register(RecipientFavorit)
admin.site.register(OpeningHours)
