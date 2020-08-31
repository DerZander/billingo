from django.contrib import admin


# Register your models here.
from organisations.models import Log, Feedback, FeedbackType, Newsletter, Checklist, ChecklistJob, Site

admin.site.register(Log)
admin.site.register(Feedback)
admin.site.register(FeedbackType)
admin.site.register(Newsletter)
admin.site.register(Checklist)
admin.site.register(ChecklistJob)
admin.site.register(Site)
