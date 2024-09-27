from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login as auth_login
from .decorators import login_not_required
from django.contrib.auth.models import User
from .models import Profile
from survey.models import Office
from django.contrib.auth.decorators import user_passes_test
from django.core.paginator import Paginator
from .forms import UserCreateForm
from django.contrib.auth import logout


@login_not_required
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            return redirect('/survey') 
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('/auth/login/')

def is_superuser(user):
    return user.is_superuser


@user_passes_test(is_superuser)
def create_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            office = form.cleaned_data['office']
            Profile.objects.create(user=user, office=office)
            return redirect('user_list')
    else:
        form = UserCreateForm()
    return render(request, 'create_user.html', {'form': form})


@user_passes_test(is_superuser)
def user_list(request):
    search_term = request.GET.get('search', '')
    selected_office = request.GET.get('office', '')

    user_list = User.objects.filter(is_superuser=False)
    
    if search_term:
        user_list = user_list.filter(username__icontains=search_term)
    
    if selected_office:
        user_list = user_list.filter(profile__office_id=selected_office)

    offices = Office.objects.all()

    paginator = Paginator(user_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'user_list.html', {'page_obj': page_obj, 'offices': offices, 'search_term': search_term, 'selected_office': selected_office})


@user_passes_test(is_superuser)
def edit_user(request, user_id):
    edit_user_instance = get_object_or_404(User, id=user_id)
    profile = edit_user_instance.profile
    if request.method == 'POST':
        form = UserCreateForm(request.POST, instance=edit_user_instance)
        if form.is_valid():
            form.save()
            profile.office = form.cleaned_data['office']
            profile.save()
            return redirect('user_list')
    else:
        form = UserCreateForm(instance=edit_user_instance)
    return render(request, 'edit_user.html', {'form': form, 'edit_user_instance': edit_user_instance, 'current_user': request.user})
