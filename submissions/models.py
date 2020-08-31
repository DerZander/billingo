from django.db import models


class Submission(models.Model):
    submissiondate = models.CharField(max_length=100)
    total_amount = models.DecimalField(default=0.00,null=True, blank=True, max_digits=10, decimal_places=2)
    submitted_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(to='users.CustomUser', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "{0}".format(self.submissiondate)

