# Generated by Django 4.0.2 on 2022-04-21 13:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dbadmin', '0002_alter_branch_options_alter_department_options_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='branch',
            options={'default_permissions': (), 'permissions': (('add_branch', 'Добавление отдела'), ('delete_branch', 'Удаление отдела'))},
        ),
        migrations.AlterModelOptions(
            name='department',
            options={'default_permissions': (), 'permissions': (('add_department', 'Добавление департамента'), ('delete_department', 'Удаление департамента'))},
        ),
        migrations.AlterModelOptions(
            name='directory',
            options={'default_permissions': (), 'permissions': (('add_directory', 'Добавление дирекции'), ('delete_directory', 'Удаление дирекции'))},
        ),
        migrations.AlterModelOptions(
            name='position',
            options={'default_permissions': (), 'permissions': (('add_position', 'Добавление должности'), ('delete_position', 'Удаление должности'))},
        ),
        migrations.AlterModelOptions(
            name='service',
            options={'default_permissions': (), 'permissions': (('add_service', 'Добавление службы/направления/управления'), ('delete_service', 'Удаление службы/направления/управления'))},
        ),
        migrations.AlterModelOptions(
            name='worker',
            options={'default_permissions': (), 'permissions': (('download_data', 'Выгрузка данных'), ('change_worker', 'Изменение данных сотрудника'))},
        ),
    ]
