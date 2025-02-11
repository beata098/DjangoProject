# Generated by Django 5.1.5 on 2025-02-11 13:12

import datetime
import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tracker', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='TrainingDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_number', models.IntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='workout',
            name='exercise',
        ),
        migrations.RemoveField(
            model_name='workout',
            name='reps',
        ),
        migrations.RemoveField(
            model_name='workout',
            name='sets',
        ),
        migrations.RemoveField(
            model_name='workout',
            name='weight',
        ),
        migrations.AlterField(
            model_name='workout',
            name='date',
            field=models.DateField(blank=True, default=datetime.datetime.now, null=True),
        ),
        migrations.AlterField(
            model_name='workout',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='BodyMeasurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(blank=True, default=datetime.datetime.now, null=True)),
                ('weight', models.FloatField()),
                ('chest', models.FloatField(blank=True, null=True)),
                ('waist', models.FloatField(blank=True, null=True)),
                ('hips', models.FloatField(blank=True, null=True)),
                ('arms', models.FloatField(blank=True, null=True)),
                ('legs', models.FloatField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Exercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nazwa', models.CharField(default='cwiczenie', max_length=100, verbose_name='Nazwa ćwiczenia')),
                ('serie', models.IntegerField(default=3, verbose_name='Liczba serii')),
                ('powtorzenia', models.IntegerField(default=12, verbose_name='Liczba powtórzeń')),
                ('training_day', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='exercises', to='tracker.trainingday')),
            ],
        ),
        migrations.AddField(
            model_name='workout',
            name='training_day',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker.trainingday'),
        ),
        migrations.CreateModel(
            name='TrainingPlan',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('plan_type', models.CharField(choices=[('masa', 'Plan na masę'), ('redukcja', 'Plan na redukcję'), ('utrzymanie', 'Plan na utrzymanie')], max_length=20)),
                ('days_per_week', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(7)], verbose_name='Dni treningowe w tygodniu')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='trainingday',
            name='plan',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='training_days', to='tracker.trainingplan'),
        ),
        migrations.AddField(
            model_name='workout',
            name='plan',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='tracker.trainingplan'),
        ),
        migrations.CreateModel(
            name='WorkoutExercise',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default=None, max_length=255)),
                ('serie', models.IntegerField(default=None)),
                ('powtorzenia', models.IntegerField(default=None)),
                ('ciezar', models.FloatField(default=0.0)),
                ('exercise', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='tracker.exercise')),
                ('workout', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='exercises', to='tracker.workout')),
            ],
        ),
    ]
