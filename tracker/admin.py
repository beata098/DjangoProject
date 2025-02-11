from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Workout, Exercise, BodyMeasurement, WorkoutExercise


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    list_display = ['user', 'plan', 'training_day', 'date']

@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("nazwa", "serie", "powtorzenia")  # ✅ poprawne pola

@admin.register(WorkoutExercise)
class WorkoutExerciseAdmin(admin.ModelAdmin):
    list_display = ('name', 'serie', 'powtorzenia', 'ciezar')

@admin.register(BodyMeasurement)
class BodyMeasurementAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'weight')
