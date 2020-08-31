from io import BytesIO

from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import F, Q
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from invoices.models import Invoice
from organisations.models import Log
from .models import *
from .forms import RecipientSearchForm, RecipientForm, RecipientTypeForm


@login_required
def doctor_index(request):
    context = {'recipients': Recipient.objects.filter(active=True).order_by('name'), 'recipientfavorit': [],
               'recipienttypes': RecipientType.objects.all(), 'invoices': Invoice.objects.filter(user=request.user) , 'navtitle': "Träger"}

    for doc in RecipientFavorit.objects.filter(user=request.user):
        context['recipientfavorit'].append(doc.recipient.id)
    if request.method == "GET":
        searchform = RecipientSearchForm(request.GET)
    else:
        searchform = RecipientSearchForm()
    recipient_query = Q(active=True)
    if searchform['recipient_name'].data:
        recipient_query.add(Q(name__icontains=searchform['recipient_name'].data), Q.AND)
    if searchform['favorit'].data:
        recipient_query.add(Q(id__in=context['recipientfavorit'])|Q(user=request.user), Q.AND)
    if searchform['recipient_type'].value():
        recipient_query.add(Q(recipienttype=RecipientType.objects.get(id=searchform['recipient_type'].data)), Q.AND)
    context['recipients'] = Recipient.objects.filter(recipient_query).order_by('name')

    context['searchform'] = searchform
    return render(request=request, template_name="recipients/index.html", context=context)

@login_required
def doctor_add(request):
    if request.method == "POST":
        form = RecipientForm(request.POST)
        if form.is_valid():
            recipient = form.save(commit=False)
            recipient.user = request.user
            recipient.save()
            messages.success(request, "Arzt erfolgreich erstellt.")
            RecipientFavorit(user=request.user, recipient=Recipient.objects.get(id=recipient.pk)).save()
            Log(user=request.user, site="Recipient", type=Log.choice_type.CREATE, object_id=recipient.pk).save()
            return redirect(reverse('recipients:doctor_index'))
    else:
        form = RecipientForm()
    context = {'doctortypes': RecipientType.objects.all(), 'form': form, 'navtitle': 'Träger hinzufügen'}
    return render(request=request, template_name='recipients/form.html', context=context)

@login_required
def doctor_edit(request, pk):
    cur_doctor = get_object_or_404(Recipient, pk=pk)
    if cur_doctor.user == request.user or request.user.is_superuser:
        if request.method == "POST":
            form = RecipientForm(request.POST, instance=cur_doctor)
            if form.is_valid():
                Log(user=request.user, site="Recipient", type=Log.choice_type.EDIT, object_id=pk).save()
                doctor = form.save(commit=False)
                doctor.save()
                messages.success(request, "Arzt erfolgreich bearbeitet.")
                return redirect(reverse('recipients:doctor_index'))
        else:
            form = RecipientForm(instance=cur_doctor)
        context = {'doctortypes': RecipientType.objects.all(), 'form': form, 'navtitle': 'Träger bearbeiten'}
        return render(request=request, template_name='recipients/form.html', context=context)
    else:
        return redirect('home')

@login_required
def doctor_delete(request, pk):
    cur_doctor = get_object_or_404(Recipient, pk=pk)
    if cur_doctor.user == request.user or request.user.is_superuser:
        if cur_doctor.active:
            Log(user=request.user, site="Recipient", type=Log.choice_type.DELETE, object_id=pk).save()
            cur_doctor.active = False
            cur_doctor.save()
            messages.success(request, "Arzt inaktiv gesetzt.")
        return redirect(reverse('recipients:doctor_index'))
    else:
        return redirect('home')

@login_required
def doctor_user_favorit(request, recipient):
    if RecipientFavorit.objects.filter(user=request.user, recipient=recipient).count() > 0:
        if Invoice.objects.filter(invoice_doctor=recipient).count() == 0:
            RecipientFavorit.objects.get(user=request.user, recipient=recipient).delete()
            messages.success(request, "Träger erfolgreich von Ihrer Liste gelöscht.")
        else:
            messages.warning(request, "Diesen Träger kannst du nicht von deiner Liste entfernen, da Rechnungen von Ihm im System sind.")
    else:
        recipient_id = Recipient.objects.get(pk=recipient)
        RecipientFavorit(user=request.user, recipient=recipient_id).save()
        messages.success(request, "Träger erfolgreich zu Ihrer Liste hinzugefügt.")
    return redirect(request.META['HTTP_REFERER'])

# def type_import(request):
#     if request.method == 'POST':
#         form = RecipientTypeForm(request.POST, request.FILES)
#         #if form.is_valid():
#         print(request.FILES)
#         # file_in_memory = request.FILES['file'].read()
#         # wb = load_workbook(filename=BytesIO(file_in_memory))
#         # ws = wb.active
#         # print(ws.cell(row=1, column=1).value)
#         # wb.close()
#         #pass
#         #else:
#         #    print(False)
#         return redirect(reverse('recipients:doctor_index'))
#     else:
#         form = RecipientTypeForm()
#     context = {'navittle':'Spezifiktaionen laden', 'form':form}
#     return render(request=request, template_name='recipients/types/edit.html', context=context)