from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import user_passes_test
from authentication import views
from office .models import Office, Service
from .forms import OfficeForm, ServiceForm


@user_passes_test(views.is_superuser)
def office_list(request):
    offices = Office.objects.all()
    return render(request, 'office_list.html', {'offices': offices})

@user_passes_test(views.is_superuser)
def office_create(request):
    form = OfficeForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('office_list')
    return render(request, 'office_create.html', {'form': form})

@user_passes_test(views.is_superuser)
def office_edit(request, office_id):
    office = get_object_or_404(Office, id=office_id)
    
    # Check if the user is a superuser or assigned to the office
    if not (request.user.is_superuser or (request.user.profile.office == office)):
        return redirect('/')  # Redirect to a safe page or show an error message

    # Pass the office instance to the form for editing
    form = OfficeForm(request.POST or None, instance=office)
    
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('office_list')

    context = {
        'form': form,
        'office': office,
    }
    return render(request, 'office_edit.html', context)


@user_passes_test(views.is_superuser)
def office_services(request, office_id):
    office = get_object_or_404(Office, id=office_id)
    
    # Check if the user has permission to view services for this office
    if not (request.user.is_superuser or (request.user.profile.office == office)):
        return redirect('/')
    
    # Get the list of services associated with the office
    services = Service.objects.filter(office=office)
    
    # Handle service creation
    form = ServiceForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        new_service = form.save(commit=False)
        new_service.office = office  # Assign the service to the correct office
        new_service.save()
        return redirect('office_services', office_id=office.id)

    context = {
        'office': office,
        'services': services,
        'form': form,  # Pass the form to the template for modal use
    }
    
    return render(request, 'office_services.html', context)

@user_passes_test(views.is_superuser)
def office_delete(request, office_id):
    office = get_object_or_404(Office, id=office_id)
    
    if not (request.user.is_superuser or (request.user.profile.office == office)):
        return redirect('/')  # Redirect to a safe page or show an error message

    if request.method == "POST":
        office.delete()
        return redirect('office_list')

    return render(request, 'office_confirm_delete.html', {'office': office})

@user_passes_test(views.is_superuser)
def delete_service(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    if request.method == 'POST':
        service.delete()
        return redirect('office_services', office_id=service.office.id)
    
    return redirect('office_services', office_id=service.office.id)


def office_create_service(request, office_id):
    office = Office.objects.get(id=office_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST)
        if form.is_valid():
            service = form.save(commit=False)
            service.office = office  # Assign the service to the office
            service.save()
            return redirect('office_services', office_id=office_id)
    else:
        form = ServiceForm()
    return render(request, 'create_service.html', {'form': form, 'office': office})

def service_edit(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    if request.method == 'POST':
        form = ServiceForm(request.POST, instance=service)
        if form.is_valid():
            form.save()
            return redirect('office_services', office_id=service.office.id)  # Redirect to the office services list
    else:
        form = ServiceForm(instance=service)
    
    return render(request, 'edit_service.html', {'form': form, 'service': service})
