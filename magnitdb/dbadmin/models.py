from argparse import MetavarTypeHelpFormatter
from django.db import models

# Create your models here.
class Directory(models.Model):
    name = models.CharField('Дирекция', max_length=128)
    
    def __str__(self):
        return self.name

class Department(models.Model):
    name = models.CharField('Департамент', max_length=128)

    def __str__(self):
        return self.name

class Service(models.Model):
    name = models.CharField('Служба/Направление/Управление', max_length=128)

    def __str__(self):
        return self.name

class Branch(models.Model):
    name = models.CharField('Отдел', max_length=128)

    def __str__(self):
        return self.name

class Position(models.Model):
    name = models.CharField('Должность', max_length=128)

    def __str__(self):
        return self.name

class Worker(models.Model):
    full_name = models.CharField('ФИО', max_length=256)
    work_phone = models.CharField('Номер рабочего телефона', max_length=16)
    cell_phone = models.CharField('Номер сотового телефона', max_length=16)

    directory = models.ForeignKey(Directory, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.CASCADE)
    branch = models.ForeignKey(Branch, on_delete=models.CASCADE)
    position = models.ForeignKey(Position, on_delete=models.CASCADE)

    def __str__(self):
        return self.full_name

