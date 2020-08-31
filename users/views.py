from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login

from django.urls import reverse
from django.shortcuts import render, redirect, get_object_or_404

from .forms import CustomUserChangeForm, UserSignInForm

from .models import CustomUser

def register(request):
    if request.method == "POST":
        form = UserSignInForm(request.POST)
        if form.is_valid():
            CustomUser.objects.create_user(request.POST['username'], request.POST['email'], request.POST['password1'])
            messages.success(request, "Sie sind registriert. Willkommen im Rechnungstool.")
            user = authenticate(username = request.POST['username'],password = request.POST['password1'])
            if user is not None:
                if user.is_active:
                    auth_login(request, user)
            return redirect(reverse('home'))
        else:
            messages.warning(request, form.errors)
    else:
        form = UserSignInForm()

    context = {'navtitle': 'Registrieren Sie sich und legen sie danach los', 'form':form}
    return render(request=request, template_name='users/sign/sign_up_form.html', context=context)

def login(request):
    if request.method == "POST":
        user = authenticate(username=request.POST['username'],password=request.POST['password'])
        if user is not None:
            if user.is_active:
                auth_login(request, user)
    return redirect(reverse('home'))

def profile_show(request):
    profile = get_object_or_404(CustomUser, pk=request.user.id)
    context = {'navtitle':'Dein Profil', 'user': CustomUser.objects.get(id=request.user.id),'form': CustomUser.objects.get(id=request.user.id), 'edit':False}
    return render(request, template_name='users/show.html', context=context)

def profile_edit(request):
    profile = get_object_or_404(CustomUser, pk=request.user.id)
    if request.method == "POST":
        form = CustomUserChangeForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.complete = True
            profile.save()
            return redirect(reverse('users:profile_show'))
    else:
        form = CustomUserChangeForm(instance=profile)

    context = {'navtitle':'Dein Profil bearbeiten', 'user': CustomUser.objects.get(id=request.user.id), 'form':form, 'edit':True}
    return render(request, template_name='users/edit.html', context=context)
