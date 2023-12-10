# Generated by Django 4.0.1 on 2022-04-13 06:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('task', '0002_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='description',
            field=models.TextField(db_column='Description', null=True),
        ),
        migrations.AlterField(
            model_name='task',
            name='status',
            field=models.ForeignKey(db_column='StatusID', null=True, on_delete=django.db.models.deletion.SET_NULL, to='task.status'),
        ),
        migrations.AlterField(
            model_name='task',
            name='time_estimation',
            field=models.TimeField(null=True),
        ),
    ]
