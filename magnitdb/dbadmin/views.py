from django.core.paginator import Paginator
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.template import loader
from django.urls import reverse
from django.contrib.auth import authenticate
from django.contrib.auth import login as djangologin
from django.contrib.auth import logout as djangologout
from django.contrib.auth.decorators import login_required
from .models import *
from openpyxl import Workbook
from datetime import datetime

LOGIN_URL = 'dbadmin:login'
ROWS_A_PAGE = 2

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


@login_required
def index(request):
    template = loader.get_template('dbadmin/index.html')
    context = {}
    return HttpResponse(template.render(context, request))


@login_required
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
    
    verbose_names = [model._meta.get_field('name').verbose_name for model in models]
    objects = [model.objects.all().order_by('name') for model in models]
    GET = [list(map(int, request.GET.getlist(filter))) for filter in filters]

    paginator = Paginator(workers, ROWS_A_PAGE) # Show 25 contacts per page.

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    template = loader.get_template('dbadmin/download.html')
    context = {
        'workers': workers,
        'Models': list(zip(filters, models, objects, verbose_names, GET)),
        'page_obj': page_obj,
    }

    print(request.build_absolute_uri())

    return HttpResponse(template.render(context, request))


@login_required
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


def _dispatch_model(model):
    if model == "directory":
        label_text = "Название дирекции"
        verbose_name = "Дирекция" 
        verbose_name_whom = "Дирекцию"
        plural_postfix = "а" #  postfix for the "добавлен" word
        type = Directory
    elif model == "department":
        label_text = "Название департамента"
        verbose_name = "Департамент"
        verbose_name_whom = "Департамент"
        plural_postfix = ""
        type = Department
    elif model == "service":
        label_text = "Название службы/направления/управления"
        verbose_name = "Служба/Направление/Управление"
        verbose_name_whom = "Службу/Направление/Управление"
        plural_postfix = "а(-о)"
        type = Service
    elif model == "branch":
        label_text = "Название отдела"
        verbose_name = "Отдел"
        verbose_name_whom = "Отдел"
        plural_postfix = ""
        type = Branch
    elif model == "position":
        label_text = "Название должности"
        verbose_name = "Должность"
        verbose_name_whom = "Должность"
        plural_postfix = "а"
        type = Position
    else:
        raise Http404()
    return label_text, verbose_name, verbose_name_whom, plural_postfix, type

was_add_succ = False
last_obj_was_add = ""

@login_required
def add(request, model):
    global was_add_succ, last_obj_was_add
    main_view = "add_" + model

    label_text, verbose_name, verbose_name_whom, plural_postfix, type = _dispatch_model(model)

    template = loader.get_template('dbadmin/add_generic.html')
    context = {
        'whom': verbose_name_whom,
        'mainview': main_view,
        'model': model,
        'labeltext': label_text,
    }

    if was_add_succ:
        context['msg'] = f"{verbose_name} \"{last_obj_was_add}\" успешно добавлен{plural_postfix}."
        context['err'] = False
        was_add_succ = False

    return HttpResponse(template.render(context, request))


@login_required
def add_save(request, model):
    global was_add_succ, last_obj_was_add
    main_view = "add_" + model

    label_text, verbose_name, verbose_name_whom, plural_postfix, type = _dispatch_model(model)

    name = request.POST.get('name', None)
    template = loader.get_template('dbadmin/add_generic.html')

    if name is None:
        raise Http404()

    if name == "":
        context = {
            'whom': verbose_name_whom,
            'mainview': main_view,
            'model': model,
            'labeltext': label_text,
            'msg': f"Произошла ошибка: поле \"{label_text}\" пусто.",
            'err': True
        }
        return HttpResponse(template.render(context, request))

    obj = type(name=name)
    obj.save()

    was_add_succ = True
    last_obj_was_add = obj.name

    return HttpResponseRedirect(reverse('dbadmin:add', args=[model]))

was_delete_succ = False
last_obj_was_delete = ""

@login_required
def delete(request, model):
    global was_delete_succ, last_obj_was_add
    main_view = "delete_" + model

    label_text, verbose_name, verbose_name_whom, plural_postfix, type = _dispatch_model(model)

    template = loader.get_template('dbadmin/delete_generic.html')

    context = {
        'whom': verbose_name_whom,
        'mainview': main_view,
        'model': model,
        'labeltext': label_text,
        'objects': type.objects.all()
    }

    if was_delete_succ:
        context['msg'] = f"{verbose_name} \"{last_obj_was_delete}\" успешно удален{plural_postfix}."
        context['err'] = False
        was_delete_succ = False

    return HttpResponse(template.render(context, request))

@login_required
def delete_save(request, model):
    global was_delete_succ, last_obj_was_delete
    main_view = "delete_" + model

    label_text, verbose_name, verbose_name_whom, plural_postfix, type = _dispatch_model(model)

    obj_id = request.POST.get('objid', None)
    template = loader.get_template('dbadmin/delete_generic.html')

    if obj_id is None:
        raise Http404()

    context = {
        'whom': verbose_name_whom,
        'mainview': main_view,
        'model': model,
        'labeltext': label_text,
        'objects': type.objects.all()
    }

    obj = type.objects.get(pk=obj_id)
    kwargs = {}
    kwargs[model + '_id'] = obj_id
    if Worker.objects.filter(**kwargs):
        context['msg'] = 'Существуют работники, для которых ' + verbose_name + " - " + obj.name + "."
        context['err'] = True
        return HttpResponse(template.render(context, request))

    obj.delete()

    was_delete_succ = True
    last_obj_was_delete = obj.name

    return HttpResponseRedirect(reverse('dbadmin:delete', args=[model]))


def login(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dbadmin:index'))

    template = loader.get_template('dbadmin/login.html')
    context = {}
    return HttpResponse(template.render(context, request))
    

def login_confirm(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('dbadmin:index'))

    username = request.POST.get('username', None)
    password = request.POST.get('password', None)
    
    user = authenticate(username=username, password=password)

    if user is not None:
        djangologin(request, user)
        return HttpResponseRedirect(reverse('dbadmin:index'))

    template = loader.get_template('dbadmin/login.html')
    context = {
        'msg': "Неверный логин или пароль."
    }
    return HttpResponse(template.render(context, request))


@login_required
def logout(request):
    djangologout(request)
    return HttpResponseRedirect(reverse('dbadmin:login'))