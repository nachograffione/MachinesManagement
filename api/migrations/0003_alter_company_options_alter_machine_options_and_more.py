# Generated by Django 4.0.5 on 2022-06-10 20:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0002_remove_machine_active_machine_deleted'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='company',
            options={'verbose_name_plural': 'Companies'},
        ),
        migrations.AlterModelOptions(
            name='machine',
            options={'verbose_name_plural': 'Machines'},
        ),
        migrations.AlterModelOptions(
            name='machineclass',
            options={'verbose_name_plural': 'MachineClasses'},
        ),
        migrations.AlterModelOptions(
            name='workingdata',
            options={'verbose_name_plural': 'WorkingDatas'},
        ),
    ]
