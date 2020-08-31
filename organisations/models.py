from django.db import models


# Create your models here.
class Log(models.Model):
    class choice_type(models.TextChoices):
        CREATE = 'ADD', 'Create'
        EDIT = 'EDT', 'Edit'
        DELETE = 'DEL', 'Delete'
        QUESTION = 'QUE', 'Question'
        NOTHING = 'NOT', 'Nothing'

    site = models.CharField(max_length=30)
    type = models.CharField(max_length=3, choices=choice_type.choices, default=choice_type.NOTHING)
    object_id = models.IntegerField(null=True, blank=True)
    message = models.TextField(null=True, blank=True)

    user = models.ForeignKey(to='users.CustomUser', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "<{0}>[{1}]{2}:{3}".format(self.user, self.type, self.site, self.object_id)


class Feedback(models.Model):
    type = models.ForeignKey(to='FeedbackType', on_delete=models.SET_NULL, null=True)
    title = models.CharField(max_length=50)
    message = models.TextField(null=True, blank=True)

    user = models.ForeignKey(to='users.CustomUser', on_delete=models.SET_NULL, null=True)
    date = models.DateTimeField(auto_now_add=True)
    done = models.BooleanField()

    def __str__(self):
        return "[{0}]{1}:{2}".format(self.user, self.title, self.message)


class FeedbackType(models.Model):
    name = models.SlugField(unique=True)
    description = models.TextField(null=True, blank=True)
    for_users = models.BooleanField()

    def __str__(self):
        return self.name


class Newsletter(models.Model):
    title = models.CharField(max_length=255)
    type = models.ForeignKey(to='FeedbackType', on_delete=models.SET_NULL, null=True)
    message = models.TextField()
    published_date = models.DateField(auto_now=True)
    end_date = models.DateField()

    def __str__(self):
        return self.title

class Site(models.Model):
    name = models.CharField(max_length=255, unique=True)
    ger_name = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name


class ChecklistJob(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    prio = models.IntegerField()
    site = models.ForeignKey(to='Site', on_delete=models.CASCADE, null=True, blank=True)
    link = models.CharField(max_length=256, null=True, blank=True)
    def __str__(self):
        return self.name

class Checklist(models.Model):
    user = models.ForeignKey(to='users.CustomUser', on_delete=models.CASCADE)
    job = models.ForeignKey(to='ChecklistJob', on_delete=models.CASCADE)
    done = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user}:{self.job}"
