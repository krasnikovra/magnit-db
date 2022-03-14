from msilib.schema import Directory
from django.contrib import admin
from .models import Directory, Branch, Department, Service, Position, Worker

# Register your models here.
admin.site.register(Directory)
admin.site.register(Department)
admin.site.register(Service)
admin.site.register(Branch)
admin.site.register(Position)
admin.site.register(Worker)