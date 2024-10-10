from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test, login_required
from authentication import utils
from office .models import Office, Service
from .forms import OfficeForm, ServiceForm
from authentication.utils import has_role

@login_required(login_url='login')
@user_passes_test(lambda user: user.is_superuser or has_role(user, ['admin']))
def office_list(request):
    offices = Office.objects.all()
    return render(request, 'office_list.html', {'offices': offices})

@login_required(login_url='login')
@user_passes_test(lambda user: user.is_superuser or has_role(user, ['admin']))
def office_create(request):
    form = OfficeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('office_list')
    return render(request, 'office_create.html', {'form': form})

@login_required(login_url='login')
@user_passes_test(lambda user: user.is_superuser or has_role(user, ['admin']))
def office_edit(request, office_id):
    office = get_object_or_404(Office, id=office_id)
    form = OfficeForm(request.POST or None, instance=office)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('office_list')
    context = {
        'form': form,
        'office': office,
    }
    return render(request, 'office_edit.html', context)

@login_required(login_url='login')
@user_passes_test(lambda user: user.is_superuser or has_role(user, ['admin']))
def office_services(request, office_id):
    office = get_object_or_404(Office, id=office_id)
    services = Service.objects.filter(office=office)
    form = ServiceForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        new_service = form.save(commit=False)
        new_service.office = office 
        new_service.save()
        return redirect('office_services', office_id=office.id)
    context = {
        'office': office,
        'services': services,
        'form': form, 
    }
    return render(request, 'office_services.html', context)

@login_required(login_url='login')
@user_passes_test(lambda user: user.is_superuser or has_role(user, ['admin']))
def office_delete(request, office_id):
    office = get_object_or_404(Office, id=office_id) 
    if request.method == "POST":
        office.delete()
        return redirect('office_list')
    return render(request, 'office_confirm_delete.html', {'office': office})

@login_required(login_url='login')
@user_passes_test(lambda user: user.is_superuser or has_role(user, ['admin']))
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        service.delete()
        return redirect('office_services', office_id=service.office.id)
    return redirect('office_services', office_id=service.office.id)


@login_required(login_url='login')
@user_passes_test(lambda user: user.is_superuser or has_role(user, ['admin']))
def office_create_service(request, office_id):
    office = Office.objects.get(id=office_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.office = office
            service.save()
            return redirect('office_services', office_id=office_id)
    else:
        form = ServiceForm()
    return render(request, 'create_service.html', {'form': form, 'office': office})


@login_required(login_url='login')
@user_passes_test(lambda user: user.is_superuser or has_role(user, ['admin']))
def service_edit(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('office_services', office_id=service.office.id)
    else:
        form = ServiceForm(instance=service)
    return render(request, 'edit_service.html', {'form': form, 'service': service})
