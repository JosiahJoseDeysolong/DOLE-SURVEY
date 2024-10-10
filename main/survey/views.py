from django.shortcuts import render, redirect
from .forms import SurveyForm
from office.models import Service
from django.http import JsonResponse

def survey_index(request):
    return render(request, 'survey_index.html')

def survey(request):
    office_id = request.POST.get('office')
    form = SurveyForm(request.POST or None, office_id=office_id)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect('survey_success')
    return render(request, 'survey_form.html', {'form': form})

def survey_success(request):
    return render(request, 'survey_success.html')

def get_services(request, office_id):
    services = Service.objects.filter(office_id=office_id).values('id', 'service_name')
    return JsonResponse({'services': list(services)})
