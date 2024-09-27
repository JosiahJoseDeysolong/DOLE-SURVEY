from django.shortcuts import render, redirect, get_object_or_404
from survey.models import Survey
from office .models import Office, Service
from django.db.models import Avg, Count
from django.contrib.auth.decorators import login_required
import openpyxl
from django.http import HttpResponse
from openpyxl.utils import get_column_letter
import csv
from django.db.models import Q
from django.core.paginator import Paginator
import pandas as pd

@login_required(login_url='login')
def export_filtered_data(request):
    service = request.GET.get('service')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    
    queryset = Survey.objects.all()
    
    if service:
        queryset = queryset.filter(service_id=service)
    
    if start_date and end_date:
        queryset = queryset.filter(date__range=[start_date, end_date])

    # Create a DataFrame from the queryset
    data = [{
        'Date': survey.date,
        'Service': survey.service.service_name,
        'Name': survey.name,
        'Contact Number': survey.contact_number,
        'Email': survey.email,
        'Client Type': survey.client_type,
        'Gender': survey.sex,
        'Age': survey.age,
        'Region': survey.region,
        'Suggestions': survey.suggestions,
        'CC1': survey.cc1,
        'CC2': survey.cc2,
        'CC3': survey.cc3,
        'SQD0': survey.sqd0,
        'SQD1': survey.sqd1,
        'SQD2': survey.sqd2,
        'SQD3': survey.sqd3,
        'SQD4': survey.sqd4,
        'SQD5': survey.sqd5,
        'SQD6': survey.sqd6,
        'SQD7': survey.sqd7,
        'SQD8': survey.sqd8,
    } for survey in queryset]

    df = pd.DataFrame(data)

    # Create a response object for the Excel file
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = f'attachment; filename="{start_date}_to_{end_date}.xlsx"'

    # Write the DataFrame to an Excel file
    with pd.ExcelWriter(response, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Surveys')

        # Access the workbook and the worksheet
        workbook = writer.book
        worksheet = writer.sheets['Surveys']

        # Adjust the width of the columns
        column_widths = {
            'A': 15,  # Date
            'B': 25,  # Service
            'C': 20,  # Name
            'D': 20,  # Contact Number
            'E': 30,  # Email
            'F': 15,  # Client Type
            'G': 10,  # Gender
            'H': 10,  # Age
            'I': 20,  # Region
            'J': 50,  # Suggestions
            'K': 10,  # CC1
            'L': 10,  # CC2
            'M': 10,  # CC3
            'N': 10,  # SQD0
            'O': 10,  # SQD1
            'P': 10,  # SQD2
            'Q': 10,  # SQD3
            'R': 10,  # SQD4
            'S': 10,  # SQD5
            'T': 10,  # SQD6
            'U': 10,  # SQD7
            'V': 10,  # SQD8
        }

        for column, width in column_widths.items():
            worksheet.column_dimensions[column].width = width

    return response
 

@login_required(login_url='login')
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

    paginator = Paginator(surveys.order_by('id'), 20)
    page_number = request.GET.get('page')
    page_surveys = paginator.get_page(page_number)

    statistics = surveys.aggregate(
        avg_sqd0=Avg('sqd0'),
        avg_sqd1=Avg('sqd1'),
        avg_sqd2=Avg('sqd2'),
    )

    client_type_stats = surveys.values('client_type').annotate(count=Count('client_type'))
    sex_stats = surveys.values('sex').annotate(count=Count('sex'))

    context = {
        'office': office,
        'surveys': page_surveys,  
        'statistics': statistics,
        'client_type_stats': client_type_stats,
        'sex_stats': sex_stats,
        'services': services,
        'selected_service': selected_service,
        'paginator': paginator,
        'search_query': search_query,
    }
    return render(request, 'survey_statistics.html', context)


@login_required(login_url='login')
def survey_list(request):
    if request.user.is_superuser:
        offices = Office.objects.all()
    else:
        offices = Office.objects.filter(id=request.user.profile.office.id)
    return render(request, 'survey_list.html', {'offices': offices})
