# Generated by Django 4.0.2 on 2022-04-21 14:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dbadmin', '0003_alter_branch_options_alter_department_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='GroupAuxPerm',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'permissions': (('add_group', 'Добавление группы'), ('delete_group', 'Удаление группы'), ('edit_group', 'Изменение группы')),
                'default_permissions': (),
            },
        ),
    ]
