from django.db import models


class Recipient(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    recipient_type = models.ForeignKey(to='RecipientType', on_delete=models.SET_NULL, null=True)
    iban = models.CharField(max_length=50, null=True, blank=True)
    street = models.CharField(max_length=100, null=True, blank=True)
    housenumber = models.CharField(max_length=50, null=True, blank=True)
    postcode = models.CharField(max_length=5, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    phonenumber = models.CharField(max_length=20, null=True, blank=True)

    active = models.BooleanField(default=True)
    user = models.ForeignKey(to='users.CustomUser', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name}"



class RecipientFavorit(models.Model):
    user = models.ForeignKey(to='users.CustomUser', on_delete=models.CASCADE, null=True)
    recipient = models.ForeignKey(to='Recipient', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.id}"


class RecipientType(models.Model):
    name = models.CharField(max_length=250, unique=True)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class OpeningHours(models.Model):
    class Weekdays(models.IntegerChoices):
        Montag = 1
        Dienstag = 2
        Mittwoch = 3
        Donnerstag = 4
        Freitag = 5
        Samstag = 6
        Sonntag = 7

    recipient = models.ForeignKey(to='Recipient', on_delete=models.CASCADE)
    day = models.IntegerField(choices=Weekdays.choices)
    beginn_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f"{self.recipient}"
