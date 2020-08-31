from datetime import date

from dateutil.relativedelta import relativedelta
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from recipients.models import Recipient, RecipientFavorit
from invoices.forms import InvoiceForm, InvoiceSearchForm
from invoices.models import Invoice
from submissions.models import Submission


@login_required
def index(request):
    context = {'navtitle': "Rechnungen"}

    doctorfavorit = []
    for doc in RecipientFavorit.objects.filter(user=request.user):
        doctorfavorit.append(doc.recipient.id)

    if request.method == 'GET':
        searchform = InvoiceSearchForm(request.GET)
    else:
        searchform = InvoiceSearchForm()
    invoice_query = Q(user=request.user)
    if searchform['invoice_data'].data:
        invoice_query.add(Q(invoice_amount__icontains=searchform['invoice_data'].data), Q.AND)
        #invoice_query.add(Q(invoice_date__icontains=form['invoice_data'].data), Q.OR)
        invoice_query.add(Q(invoice_number__icontains=searchform['invoice_data'].data), Q.OR)
    if searchform['invoice_doctor'].data:
        invoice_query.add(Q(invoice_doctor=searchform['invoice_doctor'].data), Q.AND)
    if not searchform['paid'].data:
        invoice_query.add(Q(paid_date__isnull=True), Q.AND)
        invoice_query.add(Q(submission__isnull=True), Q.OR)
    if searchform["month"].data == None:
        search_month = 0
    else:
        search_month = int(searchform["month"].data)
    if search_month > 0:
        invoice_query.add(Q(invoice_date__month=searchform["month"].data), Q.AND)

    searchform.fields["invoice_doctor"].queryset = Recipient.objects.filter(Q(id__in=doctorfavorit) | Q(user=request.user))
    context['invoices'] = Invoice.objects.filter(invoice_query)
    context['searchform'] = searchform
    return render(request=request, template_name="invoices/index.html", context=context)

@login_required
def paid(request, pk, demands):
    invoice = get_object_or_404(Invoice, pk=pk)
    if invoice.paid_date is None:
        invoice.paid_date = date.today()
    if demands == "true":
        if Submission.objects.filter(user=request.user, submitted_date=None).count() == 0:
            cur_date = date.today()
            count_submission = Submission.objects.filter(user=request.user,
                                                         submissiondate=str(cur_date.strftime("%b %Y"))).count()
            while count_submission > 0:
                cur_date = cur_date + relativedelta(months=+1)
                count_submission = Submission.objects.filter(user=request.user,
                                                             submissiondate=cur_date.strftime("%b %Y")).count()
            submission = Submission(submissiondate=str(cur_date.strftime("%b %Y")), total_amount=invoice.invoice_amount)
        else:
            submission = Submission.objects.get(user=request.user, submitted_date=None)
            submission.total_amount = submission.total_amount + invoice.invoice_amount
        invoice.submission = submission
        submission.user = request.user
        submission.save()
    invoice.save()
    return redirect(reverse('invoices:invoice_index'))


def retreat(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    if invoice.submission is not None:
        submission = Submission.objects.get(id=invoice.submission.id)
        submission.total_amount -= invoice.invoice_amount
        invoice.submission = None
        submission.save()
        invoice.save()

    return redirect(request.META['HTTP_REFERER'])


def add(request, recipient=None):
    doctorfavorit = []
    for doc in RecipientFavorit.objects.filter(user=request.user):
        doctorfavorit.append(doc.recipient.id)

    if request.method == "POST":
        form = InvoiceForm(request.POST)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.user = request.user
            invoice.save()
            return redirect(reverse('invoices:invoice_index'))
    else:
        form = InvoiceForm(initial={'invoice_doctor': recipient})
        form.fields["invoice_doctor"].queryset = Recipient.objects.filter(Q(id__in=doctorfavorit) | Q(user=request.user))
    context = {'recipients': Recipient.objects.filter(Q(id__in=doctorfavorit) | Q(user=request.user)),
               'submissions': Submission.objects.all().filter(submitted_date=None),
               'form': form,
               'navtitle': 'Rechnung hinzufügen'
               }
    return render(request, template_name='invoices/form.html', context=context)


def edit(request, pk):
    invoice = get_object_or_404(Invoice, pk=pk)
    context = {'recipients': Recipient.objects.filter(user=request.user)}
    if request.method == "POST":
        form = InvoiceForm(request.POST, instance=invoice)
        if form.is_valid():
            invoice = form.save(commit=False)
            invoice.save()
            return redirect(reverse('invoices:invoice_index'))
    else:
        form = InvoiceForm(instance=invoice)
        form.fields["invoice_doctor"].queryset = Recipient.objects.filter(user=request.user)
    context['form'] = form
    context['navtitle'] = "Rechnung bearbeiten"
    return render(request, 'invoices/form.html', context=context)


def delete(request, pk):
    if Invoice.objects.get(pk=pk).submission is None:
        try:
            Invoice.objects.get(pk=pk).delete()
        finally:
            return redirect(reverse('invoices:invoice_index'))
