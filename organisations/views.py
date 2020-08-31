from datetime import date, datetime

from dateutil.relativedelta import relativedelta
from django.db.models import Q
from django.shortcuts import render, redirect
from django.urls import reverse

from recipients.models import RecipientFavorit, Recipient
from invoices.models import Invoice
from organisations.forms import FeedbackForm
from organisations.models import Feedback, FeedbackType, Newsletter, ChecklistJob, Checklist
from submissions.models import Submission
from users.models import CustomUser


def index(request):
    context = {'feedbacks': Feedback.objects.all()}
    return render(request=request, template_name='feedbacks/index.html', context=context)

def impressum(request):
    context = {'navtitle':'Impressum'}
    return render(request=request, template_name='organisations/fixed_pages/impressum.html', context=context)

def create(request):
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            feedback = form.save(commit=False)
            feedback.user = request.user
            feedback.done = False
            feedback.save()
            return redirect(to='home')
    else:
        form = FeedbackForm()
    context = {'form': form, 'navtitle': 'Feedback geben'}
    if request.user.is_superuser:
        context['feedbacktypes'] = FeedbackType.objects.all()
    else:
        context['feedbacktypes'] = FeedbackType.objects.filter(for_users=True)
    return render(request=request, template_name='feedbacks/form.html', context=context)


def change_status(request, pk):
    feedback = Feedback.objects.get(pk=pk)
    if not feedback.done:
        feedback.done = True
        feedback.save()
        print(True)
    else:
        print(False)
    return redirect(request.META['HTTP_REFERER'])


def overview(request):
    if request.user.is_authenticated != True:
        return redirect(reverse('register'))
    context = {'newsletters': Newsletter.objects.filter(),
               'tasks': {"profile": False, "recipients": False, "invoice": False, "submission": False, 'tutorial': False}}
    tasks = context['tasks']
    if CustomUser.objects.get(id=request.user.id).complete:
        tasks['profile'] = True

    if Invoice.objects.filter(user=request.user).count() > 0:
        tasks['invoice'] = True

    recipientfavorit = []
    for recipient in RecipientFavorit.objects.filter(user=request.user):
        recipientfavorit.append(recipient.recipient.id)
    if Recipient.objects.filter(user=request.user, id__in=recipientfavorit):
        tasks['recipients'] = True

    if Submission.objects.filter(user=request.user).count() > 0:
        tasks['submission'] = True

    if tasks['profile'] and tasks['recipients'] and tasks['invoice'] and tasks['submission']:
        tasks['tutorial'] = True



    context['navtitle'] = "Überblick"
    context['invoices'] = []
    for tmp_month in range(0, 12, 1):
        var_month = date.today() - relativedelta(months=+tmp_month)
        if Invoice.objects.filter(Q(user=request.user), Q(invoice_date__month=var_month.month, invoice_date__year=var_month.year)).count() > 0:
            invoices_not_paid = Invoice.objects.filter(Q(user=request.user), Q(invoice_date__month=var_month.month, invoice_date__year=var_month.year), Q(paid_date__isnull=True))
            invoices_paid = Invoice.objects.filter(Q(user=request.user), Q(invoice_date__month=var_month.month, invoice_date__year=var_month.year), Q(paid_date__isnull=False), Q(submission__isnull=True))
            invoices_submission = Invoice.objects.filter(Q(user=request.user), Q(invoice_date__month=var_month.month, invoice_date__year=var_month.year), Q(paid_date__isnull=False), Q(submission__isnull=False))
            invoices_total = Invoice.objects.filter(Q(user=request.user), Q(invoice_date__month=var_month.month, invoice_date__year=var_month.year))
            invoice = {
                'month': var_month.strftime('%B %Y'),
                'total_not_paid': invoices_not_paid.count(),
                'total_not_submission': invoices_paid.count(),
                'total_complete': invoices_submission.count(),
                'total': invoices_total.count(),
                'total_amount_not_paid': 0,
                'total_amount_paid': 0,
                'total_amount_submission':0,
                'total_amount':0,
                'total_amount_percent_not_paid': 0,
                'total_amount_percent_paid':  0,
                'total_amount_percent_submission': 0,
            }
            for inv_np in invoices_not_paid:
                invoice['total_amount_not_paid'] += inv_np.invoice_amount
            for inv_p in invoices_paid:
                invoice['total_amount_paid'] += inv_p.invoice_amount
            for inv_s in invoices_submission:
                invoice['total_amount_submission'] += inv_s.invoice_amount
            for inv in invoices_total:
                invoice['total_amount'] += inv.invoice_amount

            invoice['total_amount_percent_not_paid'] = round((100/invoice['total_amount'])*invoice['total_amount_not_paid'], 0)
            invoice['total_amount_percent_paid'] = round((100/invoice['total_amount'])*invoice['total_amount_paid'], 0)
            invoice['total_amount_percent_submission'] = round((100/invoice['total_amount'])*invoice['total_amount_submission'], 0)
            context['invoices'].append(invoice)
    return render(request=request, template_name='organisations/homepage.html', context=context)
