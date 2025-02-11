from datetime import datetime
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


class TrainingPlan(models.Model):
    PLAN_TYPE_CHOICES = [
        ('masa', 'Plan na masę'),
        ('redukcja', 'Plan na redukcję'),
        ('utrzymanie', 'Plan na utrzymanie'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    plan_type = models.CharField(max_length=20, choices=PLAN_TYPE_CHOICES)
    days_per_week = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(7)],
        verbose_name='Dni treningowe w tygodniu'
    )

    def __str__(self):
        return self.name

class TrainingDay(models.Model):
    plan = models.ForeignKey("TrainingPlan", on_delete=models.CASCADE, related_name="training_days")
    day_number = models.IntegerField()

    def __str__(self):
        return f"Dzień {self.day_number} - {self.plan.name}"


class Exercise(models.Model):
    training_day = models.ForeignKey(TrainingDay, on_delete=models.CASCADE, null=True, blank=True, related_name='exercises')
    nazwa = models.CharField(max_length=100, verbose_name="Nazwa ćwiczenia", default="cwiczenie")
    serie = models.IntegerField(verbose_name="Liczba serii", default= 3)
    powtorzenia = models.IntegerField(verbose_name="Liczba powtórzeń", default= 12)

    def __str__(self):
        return f"{self.nazwa} - {self.serie} serii x {self.powtorzenia} powtórzeń"


class Workout(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey('TrainingPlan', on_delete=models.CASCADE, null=True, blank=True)
    training_day = models.ForeignKey('TrainingDay', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateField(null=True, blank=True, default=datetime.now)

    def __str__(self):
        return f"Trening {self.id} - {self.user.username} ({self.training_day})"


class WorkoutExercise(models.Model):
    workout = models.ForeignKey(Workout, on_delete=models.CASCADE, related_name="exercises")
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE, default=None)
    name = models.CharField(max_length=255, default=None)
    serie = models.IntegerField(default=None)
    powtorzenia = models.IntegerField(default=None)
    ciezar = models.FloatField(default=0.0)

    def __str__(self):
        return f"{self.name} - {self.serie} serii x {self.powtorzenia} powtórzeń ({self.ciezar} kg)"

class BodyMeasurement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(null=True, blank=True, default=datetime.now)
    weight = models.FloatField()
    chest = models.FloatField(null=True, blank=True)
    waist = models.FloatField(null=True, blank=True)
    hips = models.FloatField(null=True, blank=True)
    arms = models.FloatField(null=True, blank=True)
    legs = models.FloatField(null=True, blank=True)



    def __str__(self):
        return f"{self.user.username} - {self.date} - {self.weight} kg"



