from argparse import MetavarTypeHelpFormatter
from django.db import models
from django.contrib.auth.models import User, Group

# Create your models here.
class Directory(models.Model):
    name = models.CharField('Дирекция', max_length=128)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = 'Дирекция'
        default_permissions = ()
        permissions = (
            ('add_directory', 'Добавление дирекции'),
            ('delete_directory', 'Удаление дирекции'),
            ('edit_directory', 'Изменение дирекции'),
        )

class Department(models.Model):
    name = models.CharField('Департамент', max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Департамент'
        default_permissions = ()
        permissions = (
            ('add_department', 'Добавление департамента'),
            ('delete_department', 'Удаление департамента'),
            ('edit_department', 'Изменение департамента'),
        )

class Service(models.Model):
    name = models.CharField('Служба/Направление/Управление', max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Служба/Направление/Управление'
        default_permissions = ()
        permissions = (
            ('add_service', 'Добавление службы/направления/управления'),
            ('delete_service', 'Удаление службы/направления/управления'),
            ('edit_service', 'Изменение службы/направления/управления'),
        )

class Branch(models.Model):
    name = models.CharField('Отдел', max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Отдел'
        default_permissions = ()
        permissions = (
            ('add_branch', 'Добавление отдела'),
            ('delete_branch', 'Удаление отдела'),
            ('edit_branch', 'Изменение отдела'),
        )

class Position(models.Model):
    name = models.CharField('Должность', max_length=128)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Должность'
        default_permissions = ()
        permissions = (
            ('add_position', 'Добавление должности'),
            ('delete_position', 'Удаление должности'),
            ('edit_position', 'Изменение должности'),
        )

class Worker(models.Model):
    full_name = models.CharField('ФИО', max_length=256)
    work_phone = models.CharField('Номер рабочего телефона', max_length=16)
    cell_phone = models.CharField('Номер сотового телефона', max_length=16)

    directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Сотрудник'
        default_permissions = ()
        permissions = (
            ('download_data', 'Выгрузка данных'),
            ('edit_worker', 'Изменение данных сотрудника'),
            ('search_worker', 'Поиск сотрудников'),
            ('assign_group', 'Назначение групп привилегий'),            
        )

class GroupAuxPerm(models.Model):
    class Meta:
        verbose_name = 'Группа пользователей'
        default_permissions = ()
        permissions = (
            ('add_group', 'Добавление группы'),
            ('delete_group', 'Удаление группы'),
            ('edit_group', 'Изменение группы')         
        )
