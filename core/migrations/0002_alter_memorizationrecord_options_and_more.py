# Generated by Django 5.2 on 2025-05-02 17:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='memorizationrecord',
            options={'verbose_name': 'memorization record', 'verbose_name_plural': 'memorization records'},
        ),
        migrations.AddField(
            model_name='memorizationrecord',
            name='level',
            field=models.CharField(blank=True, choices=[('bad', 'Bad'), ('good', 'Good'), ('excellent', 'Excellent')], default='good', max_length=100, null=True, verbose_name='level'),
        ),
        migrations.AddField(
            model_name='student',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='notes'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='date of birth'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='education',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='education'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='job',
            field=models.CharField(blank=True, max_length=100, null=True, verbose_name='job'),
        ),
        migrations.AddField(
            model_name='teacher',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='notes'),
        ),
        migrations.AlterField(
            model_name='memorizationrecord',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='memorizationrecord',
            name='pages_memorized',
            field=models.PositiveIntegerField(verbose_name='pages memorized'),
        ),
        migrations.AlterField(
            model_name='memorizationrecord',
            name='session',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memorization_records', to='core.session', verbose_name='session'),
        ),
        migrations.AlterField(
            model_name='memorizationrecord',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='memorization_records', to='core.student', verbose_name='student'),
        ),
        migrations.AlterField(
            model_name='memorizationrecord',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated at'),
        ),
        migrations.AlterField(
            model_name='session',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='session',
            name='date',
            field=models.DateField(unique=True, verbose_name='date'),
        ),
        migrations.AlterField(
            model_name='student',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='student',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='date of birth'),
        ),
        migrations.AlterField(
            model_name='student',
            name='full_name',
            field=models.CharField(max_length=100, verbose_name='full name'),
        ),
        migrations.AlterField(
            model_name='student',
            name='phone_number',
            field=models.CharField(blank=True, max_length=15, null=True, verbose_name='phone number'),
        ),
        migrations.AlterField(
            model_name='student',
            name='teacher',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='students', to='core.teacher', verbose_name='teacher'),
        ),
        migrations.AlterField(
            model_name='student',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated at'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='created at'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='phone_number',
            field=models.CharField(max_length=15, verbose_name='phone number'),
        ),
        migrations.AlterField(
            model_name='teacher',
            name='updated_at',
            field=models.DateTimeField(auto_now=True, verbose_name='updated at'),
        ),
        migrations.DeleteModel(
            name='Attendance',
        ),
    ]
