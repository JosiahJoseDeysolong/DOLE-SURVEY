from django.shortcuts import render, redirect, get_object_or_404
from survey.models import Survey
from office .models import Office, Service
from django.db.models import Count, Sum, F
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator
from django.db.models import Count
import csv
from django.contrib.auth.decorators import login_required, user_passes_test
from authentication.utils import has_role
from .forms import SurveyEditForm

@login_required(login_url='login')
@user_passes_test(lambda user: user.is_superuser or has_role(user, ['admin', 'hr']))
def export_filtered_data(request):
    office_id = request.GET.get('office_id')
    service_id = request.GET.get('service')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    surveys = Survey.objects.filter(office_id=office_id)

    if service_id and service_id != "None":
        surveys = surveys.filter(service_id=service_id)

    if start_date:
        surveys = surveys.filter(date__gte=start_date)

    if end_date:
        surveys = surveys.filter(date__lte=end_date)

    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="filtered_survey_data.csv"'
    writer = csv.writer(response)
    writer.writerow(['Name', 'Contact Number', 'Email', 'Client Type', 'Date', 'Sex', 'Age', 'Region', 'Suggestions', 'CC1', 'CC2', 'CC3', 'Sqd0', 'Sqd1', 'Sqd2', 'Sqd3', 'Sqd4', 'Sqd5', 'Sqd6', 'Sqd7', 'Sqd8'])
    for survey in surveys:
        writer.writerow([survey.name, survey.contact_number, survey.email, survey.get_client_type_display(),
                         survey.date, survey.get_sex_display(), survey.age, survey.region, survey.suggestions,
                         survey.cc1, survey.cc2, survey.cc3, survey.sqd0, survey.sqd1, survey.sqd2, survey.sqd3,
                         survey.sqd4, survey.sqd5, survey.sqd6, survey.sqd7, survey.sqd8])
    return response

@login_required(login_url='login')
@user_passes_test(lambda user: user.is_superuser or has_role(user, ['admin', 'hr', 'employee']))
def survey_statistics(request, office_id):
    office = get_object_or_404(Office, id=office_id)
    services = Service.objects.filter(office=office)
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    selected_service = request.GET.get('service')
    search_query = request.GET.get('search', '')
    surveys = Survey.objects.filter(office=office)

    if start_date and end_date:
        surveys = surveys.filter(date__range=[start_date, end_date])

    if selected_service and selected_service != 'None':
        surveys = surveys.filter(service_id=selected_service)

    if search_query:
        surveys = surveys.filter(
            Q(name__icontains=search_query) |
            Q(email__icontains=search_query) |
            Q(contact_number__icontains=search_query)
        )

    paginator = Paginator(surveys.order_by('id'), 10)
    page_number = request.GET.get('page')
    page_surveys = paginator.get_page(page_number)
    total_surveys_count = surveys.count()
    total_score = surveys.aggregate(
        total_sqd=Sum(F('sqd0') + F('sqd1') + F('sqd2') + F('sqd3') + 
                       F('sqd4') + F('sqd5') + F('sqd6') + F('sqd7') + F('sqd8'))
    )['total_sqd'] or 0

    average_score = total_score / (total_surveys_count * 9) if total_surveys_count > 0 else 0
    average_score = round(average_score, 2)
    percentage_score = (average_score / 5) * 100
    percentage_score = round(percentage_score, 2)
    client_type_stats = surveys.values('client_type').annotate(count=Count('client_type'))
    sex_stats = surveys.values('sex').annotate(count=Count('sex'))

    context = {
        'office': office,
        'surveys': page_surveys,  
        'total_surveys_count': total_surveys_count,
        'average_score': average_score,
        'percentage_score': percentage_score,
        'client_type_stats': client_type_stats,
        'sex_stats': sex_stats,
        'services': services,
        'selected_service': selected_service,
        'paginator': paginator,
        'search_query': search_query,
    }

    return render(request, 'survey_statistics.html', context)


@login_required(login_url='login')
@user_passes_test(lambda user: user.is_superuser or has_role(user, ['admin']))
def survey_item_edit(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    office_id = survey.office.id
    
    if request.method == 'POST':
        form = SurveyEditForm(request.POST, instance=survey)
        if form.is_valid():
            form.save()
            return redirect('survey_statistics', office_id=office_id)
    else:
        form = SurveyEditForm(instance=survey)
    
    return render(request, 'survey_edit.html', {'form': form, 'survey': survey, 'office_id': office_id})


@login_required(login_url='login')
@user_passes_test(lambda user: user.is_superuser or has_role(user, ['admin']))
def survey_delete(request, survey_id):
    survey = get_object_or_404(Survey, id=survey_id)
    if request.method == 'POST':
        survey.delete()
        return redirect('survey_statistics', office_id=survey.office.id)
    return redirect('survey_statistics', office_id=survey.office.id)

@login_required(login_url='login')
@user_passes_test(lambda user: user.is_superuser or has_role(user, ['admin', 'hr', 'employee']))
def survey_list(request):
    if request.user.is_superuser or request.user.profile.role == 'admin' or request.user.profile.role == 'hr':
        offices = Office.objects.all()
    else:
        offices = Office.objects.filter(id=request.user.profile.office.id)
    return render(request, 'survey_list.html', {'offices': offices})

@login_required(login_url='login')
@user_passes_test(lambda user: user.is_superuser or has_role(user, ['admin', 'hr']))
def survey_consolidated(request):
    offices = Office.objects.all()
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    selected_service = request.GET.get('service')
    office_data = []
    for office in offices:
        surveys = Survey.objects.filter(office=office)
        if start_date and end_date:
            surveys = surveys.filter(date__range=[start_date, end_date])
        if selected_service and selected_service != 'None':
            surveys = surveys.filter(service_id=selected_service)
        total_surveys_count = surveys.count()
        total_score = surveys.aggregate(
            total_sqd=Sum(F('sqd0') + F('sqd1') + F('sqd2') + F('sqd3') +
                          F('sqd4') + F('sqd5') + F('sqd6') + F('sqd7') + F('sqd8'))
        )['total_sqd'] or 0
        average_score = total_score / (total_surveys_count * 9) if total_surveys_count > 0 else 0
        average_score = round(average_score, 2)
        percentage_score = (average_score / 5) * 100
        percentage_score = round(percentage_score, 2)
        office_data.append({
            'office': office,
            'total_surveys_count': total_surveys_count,
            'average_score': average_score,
            'percentage_score': percentage_score,
        })
    surveys = Survey.objects.all()

    if start_date and end_date:
        surveys = surveys.filter(date__range=[start_date, end_date])

    if selected_service and selected_service != 'None':
        surveys = surveys.filter(service_id=selected_service)

    paginator = Paginator(surveys.order_by('id'), 20)
    page_number = request.GET.get('page')
    page_surveys = paginator.get_page(page_number)
    total_surveys_count = surveys.count()
    total_score = surveys.aggregate(
        total_sqd=Sum(F('sqd0') + F('sqd1') + F('sqd2') + F('sqd3') +
                      F('sqd4') + F('sqd5') + F('sqd6') + F('sqd7') + F('sqd8'))
    )['total_sqd'] or 0
    average_score = total_score / (total_surveys_count * 9) if total_surveys_count > 0 else 0
    average_score = round(average_score, 2)
    percentage_score = (average_score / 5) * 100
    percentage_score = round(percentage_score, 2)
    client_type_stats = surveys.values('client_type').annotate(count=Count('client_type'))
    sex_stats = surveys.values('sex').annotate(count=Count('sex'))
    context = {
        'offices': offices,
        'office_data': office_data,
        'surveys': page_surveys,
        'total_surveys_count': total_surveys_count,
        'average_score': average_score,
        'percentage_score': percentage_score,
        'client_type_stats': client_type_stats,
        'sex_stats': sex_stats,
        'paginator': paginator,
    }
    
    return render(request, 'survey_consolidated.html', context)

