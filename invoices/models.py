from django.db import models
from recipients.models import Recipient
from submissions.models import Submission


class Invoice(models.Model):
    invoice_number = models.CharField(max_length=250)
    invoice_doctor = models.ForeignKey(to='recipients.Recipient', on_delete=models.SET_NULL, null=True, blank=True)
    invoice_date = models.DateField()
    invoice_amount = models.DecimalField(default=0.00, max_digits=10, decimal_places=2)
    description = models.TextField(null=True, blank=True)
    submission = models.ForeignKey(to='submissions.Submission', on_delete=models.SET_NULL, null=True, blank=True)
    paid_date = models.DateField(null=True, blank=True)
    user = models.ForeignKey(to='users.CustomUser', on_delete=models.CASCADE, null=True)

    def __str__(self):
        return "{0}: {1} ({2}) = paid:{3}, submission:{4}".format(self.invoice_doctor, self.invoice_number, self.invoice_amount, self.paid_date, self.submission)
