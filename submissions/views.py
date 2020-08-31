from datetime import date
from django.shortcuts import render, redirect

from django.urls import reverse

from invoices.models import Invoice
from submissions.models import Submission


def index(request):
    context = {'submissions': Submission.objects.filter(user=request.user), 'navtitle': 'Anforderungen'}
    return render(request, template_name='submissions/index.html', context=context)


def detail(request, submission_id):
    submission = Submission.objects.get(user=request.user, id=submission_id)
    invoices = Invoice.objects.filter(submission=submission.id, user=request.user)
    context = {'submission': submission, 'invoices': invoices, 'total_amount': 0,
               'total_number': invoices.count(), 'navtitle': 'Anforderungen'}
    for invoice in invoices:
        context['total_amount'] = context['total_amount'] + invoice.invoice_amount


    context['percent_30'] = context['total_amount']/100*30
    context['percent_70'] = context['total_amount']/100*70
    return render(request, template_name='submissions/detail.html', context=context)


def send(request, submission_id):
    submission = Submission.objects.get(id=submission_id)
    submission.submitted_date = date.today()
    submission.save()
    return redirect(reverse('submissions:submissions_index'))