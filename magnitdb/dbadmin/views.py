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

ROWS_A_PAGE_DOWNLOAD = 2
ROWS_A_PAGE_SEARCH = 2

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

    paginator = Paginator(workers, ROWS_A_PAGE_DOWNLOAD)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    template = loader.get_template('dbadmin/download.html')
    context = {
        'workers': workers,
        'Models': list(zip(filters, models, objects, verbose_names, GET)),
        'page_obj': page_obj,
    }

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


@login_required
def profile(request, worker_id):
    try:
        worker = Worker.objects.get(pk=worker_id)
    except Worker.DoesNotExist:
        raise Http404()
    template = loader.get_template('dbadmin/profile.html')
    models = [Position, Branch, Service, Department, Directory]
    desc_labels = [model._meta.get_field('name').verbose_name for model in models]
    desc_values = [getattr(worker, model.__name__.lower()).name for model in models]
    desc = list(zip(desc_labels, desc_values))
    context = {
        'worker': worker,
        'desc': desc
    }
    return HttpResponse(template.render(context, request))


@login_required
def search(request):
    kwargs = {}
    full_name = request.GET.get('full_name', None)
    workers_and_descs = []
    page_obj = None
    collapse_filters = True
    if full_name is not None:
        kwargs['full_name__icontains'] = full_name
        for filter in filters:
            filter_get = request.GET.getlist(filter)
            if filter_get:
                collapse_filters = False
                kwargs[filter + '__in'] = request.GET.getlist(filter)
        print(kwargs)
        workers = Worker.objects.filter(**kwargs).order_by('full_name')
        print(workers)
        desc_values = [[getattr(worker, model.__name__.lower()).name for model in models][::-1] for worker in workers]
        workers_and_descs = list(zip(workers, desc_values))

        paginator = Paginator(workers_and_descs, ROWS_A_PAGE_SEARCH)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    verbose_names = [model._meta.get_field('name').verbose_name for model in models]
    objects = [model.objects.all().order_by('name') for model in models]
    GET = [list(map(int, request.GET.getlist(filter))) for filter in filters]

    template = loader.get_template("dbadmin/search.html")
    context = {
        'collapse_filters': collapse_filters,
        'Models': list(zip(filters, models, objects, verbose_names, GET)),
        'results_count': len(workers_and_descs),
        'page_obj': page_obj,
        'full_name': full_name if full_name is not None else ''
    }
    return HttpResponse(template.render(context, request))


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