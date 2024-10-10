from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from .decorators import login_not_required
from django.contrib.auth.models import User
from .models import Profile
from survey.models import Office
from django.core.paginator import Paginator
from .forms import UserCreateForm, CustomUserChangeForm
from django.contrib.auth import logout
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import user_passes_test
from .utils import send_otp
from django.http import JsonResponse
from django.utils import timezone
from .utils import has_role


@login_not_required
def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            request.session['username'] = form.cleaned_data['username']
            send_otp(request)
            return render(request, 'login.html', {
                'form': form,
                'show_otp_modal': True,
            })
    else:
        form = AuthenticationForm()

    return render(request, 'login.html', {'form': form, 'show_otp_modal': False})

def otp(request):
    if request.method == 'POST':
        otp = request.POST.get('otp')
        username = request.session.get('username')
        otp_secret_key = request.session.get('otp_secret_key')
        otp_valid_date = request.session.get('otp_valid_date')
        stored_otp = request.session.get('otp')

        if otp_secret_key and otp_valid_date:
            valid_until = timezone.datetime.fromisoformat(otp_valid_date)
            current_time = timezone.now()

            print(f"Current Time: {current_time}")
            print(f"Valid Until: {valid_until}")
            print(f"Entered OTP: {otp}")
            print(f"Stored OTP: {stored_otp}")

            if valid_until > current_time:
                if otp == stored_otp:
                    print("OTP verified successfully.")
                    user = get_object_or_404(User, username=username)
                    auth_login(request, user)
                    request.session.pop('otp_secret_key', None)
                    request.session.pop('otp_valid_date', None)
                    request.session.pop('username', None)
                    request.session.pop('otp', None)

                    return JsonResponse({'success': True})
                else:
                    print("Invalid OTP entered.")
                    return JsonResponse({'success': False, 'error_message': 'Invalid one-time password'}, status=400)
            else:
                print("OTP has expired.")
                return JsonResponse({'success': False, 'error_message': 'One-time password has expired'}, status=400)
        else:
            print("OTP secret key or valid date not found in session.")
            return JsonResponse({'success': False, 'error_message': 'Oops, something went wrong.'}, status=400)

    return JsonResponse({'success': False, 'error_message': 'Invalid request'}, status=400)

def logout_view(request):
    logout(request)
    return redirect('/auth/login/')

@user_passes_test(lambda user: user.is_superuser or has_role(user, ['admin']))
def create_user(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            office = form.cleaned_data['office']
            role = form.cleaned_data['role']
            Profile.objects.create(user=user, office=office, role=role)
            return redirect('user_list')
    else:
        form = UserCreateForm()
    return render(request, 'create_user.html', {'form': form})

@user_passes_test(lambda user: user.is_superuser or has_role(user, ['admin']))
def user_list(request):
    search_term = request.GET.get('search', '')
    selected_office = request.GET.get('office', '')

    user_list = User.objects.filter(is_superuser=False).order_by('username')
    
    if search_term:
        user_list = user_list.filter(username__icontains=search_term)
    
    if selected_office:
        user_list = user_list.filter(profile__office_id=selected_office)

    offices = Office.objects.all()

    paginator = Paginator(user_list, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'user_list.html', {'page_obj': page_obj, 'offices': offices, 'search_term': search_term, 'selected_office': selected_office})

@user_passes_test(lambda user: user.is_superuser or has_role(user, ['admin']))
def edit_user(request, user_id):
    edit_user_instance = get_object_or_404(User, id=user_id)
    profile = edit_user_instance.profile
    
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=edit_user_instance)
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            profile.office = form.cleaned_data['office']
            profile.role = form.cleaned_data['role']
            profile.save()

            return redirect('user_list')
    else:
        form = CustomUserChangeForm(instance=edit_user_instance, initial={
            'office': profile.office,
            'role': profile.role
        })
        
    return render(request, 'edit_user.html', {'form': form, 'edit_user_instance': edit_user_instance})

@user_passes_test(lambda user: user.is_superuser or has_role(user, ['admin']))
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == "POST":
        user.delete()
        return redirect('user_list')
    return redirect('user_list')
