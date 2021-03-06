# Generated by Django 4.0.5 on 2022-06-11 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_company_deleted_company_deleted_by_cascade_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='machine',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='machineclass',
            name='name',
            field=models.CharField(max_length=50),
        ),
        migrations.AddConstraint(
            model_name='company',
            constraint=models.UniqueConstraint(condition=models.Q(('deleted__isnull', True)), fields=('name',), name='company_unique_non_deleted_name'),
        ),
        migrations.AddConstraint(
            model_name='machine',
            constraint=models.UniqueConstraint(condition=models.Q(('deleted__isnull', True)), fields=('name',), name='machine_unique_non_deleted_name'),
        ),
        migrations.AddConstraint(
            model_name='machineclass',
            constraint=models.UniqueConstraint(condition=models.Q(('deleted__isnull', True)), fields=('name',), name='machine_class_unique_non_deleted_name'),
        ),
    ]
