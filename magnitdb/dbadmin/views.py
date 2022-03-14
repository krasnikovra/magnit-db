from django.template.defaulttags import register
from django.http import HttpResponse
from django.template import loader
from .models import *
from openpyxl import Workbook
from datetime import datetime
from datetime import timedelta

# all possible filters
filters = [
    'directory_id',
    'department_id',
    'service_id',
    'branch_id',
    'position_id',
]
models = [
    Directory, 
    Department, 
    Service, 
    Branch, 
    Position
]


def index(request):
    template = loader.get_template('dbadmin/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


def download(request):
    # collecting a dict of **kwargs which is something like
    # {
    #   'directory_id__in': request.GET.getlist('directory_id')
    # }
    args = {}
    for filter in filters:
        args[filter + '__in'] = request.GET.getlist(filter)
    # if some GET params are invalid we are aborting any filtering
    workers = Worker.objects.filter(**args).order_by('full_name')

    # TODO: its quitely hard to pass 1bln table by http, so we must have some limit, i.e. first 1000 rows?
    
    verbose_names = [model._meta.get_field('name').verbose_name for model in models]
    objects = [model.objects.all() for model in models]
    GET = [list(map(int, request.GET.getlist(filter))) for filter in filters]

    template = loader.get_template('dbadmin/download.html')
    context = {
        'workers': workers,
        'Models': list(zip(filters, models, objects, verbose_names, GET)),
    }

    return HttpResponse(template.render(context, request))


def export(request):
    # collecting a dict of **kwargs which is something like
    # {
    #   'directory_id__in': request.GET.getlist('directory_id')
    # }
    args = {}
    for filter in filters:
        args[filter + '__in'] = request.GET.getlist(filter)
    workers = Worker.objects.filter(**args).order_by('full_name')

    headers = ('ID', 'ФИО', 'Номер рабочего телефона', 'Номер сотового телефона', 'Дирекция', 'Департамент', 'Служба', 'Отдел', 'Должность')
    
    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    )
    response['Content-Disposition'] = 'attachment; filename={date}-dbexport.xlsx'.format(
        date=datetime.now().strftime('%Y-%m-%d'),
    )
    workbook = Workbook()
    worksheet = workbook.active

    row_num = 1

    # Assign the titles for each cell of the header
    for col_num, column_title in enumerate(headers, 1):
        cell = worksheet.cell(row=row_num, column=col_num)
        cell.value = column_title

    # Iterate through all workers
    for worker in workers:
        row_num += 1
        
        # Define the data for each cell in the row 
        row = [
            worker.pk,
            worker.full_name,
            worker.work_phone,
            worker.cell_phone,
            worker.directory.name,
            worker.department.name,
            worker.service.name,
            worker.branch.name,
            worker.position.name,
        ]
        
        # Assign the data for each cell of the row 
        for col_num, cell_value in enumerate(row, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = cell_value

    workbook.save(response)

    return response
