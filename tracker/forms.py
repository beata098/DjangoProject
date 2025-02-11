from datetime import timezone, datetime

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.utils.timezone import now

from .models import TrainingPlan, Workout, WorkoutExercise, BodyMeasurement, Exercise
from django.core.exceptions import ValidationError



class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Hasło')
    confirm_password = forms.CharField(widget=forms.PasswordInput, label='Potwierdź hasło')

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise ValidationError("Hasła się nie zgadzają.")

        return cleaned_data


class TrainingPlanForm(forms.ModelForm):
    class Meta:
        model = TrainingPlan
        fields = ['name', 'plan_type', 'days_per_week']
        labels = {
            'name': 'Nazwa planu',
            'plan_type': 'Typ planu',
            'days_per_week': 'Dni treningowe w tygodniu',
        }

        widgets = {
            'days_per_week': forms.NumberInput(attrs={'min': 1, 'max': 7, 'required': 'required'}),
        }

    def clean_days_per_week(self):
        days = self.cleaned_data.get('days_per_week')
        if days is None or not (1 <= days <= 7):
            raise forms.ValidationError("Liczba dni musi być w przedziale od 1 do 7.")
        return days


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ["nazwa", "serie", "powtorzenia"]
        labels = {
            "nazwa": "Nazwa ćwiczenia",
            "serie": "Liczba serii",
            "powtorzenia": "Liczba powtórzeń",
        }


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ['plan', 'training_day']

class WorkoutExerciseForm(forms.ModelForm):
    class Meta:
        model = WorkoutExercise
        fields = ['name', 'serie', 'powtorzenia', 'ciezar']
        labels = {
            'name': 'Ćwiczenie',
            'serie': 'Serie',
            'powtorzenia': 'Powtórzenia',
            'ciezar': 'Ciężar (kg)',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'serie': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'powtorzenia': forms.NumberInput(attrs={'class': 'form-control', 'min': 1}),
            'ciezar': forms.NumberInput(attrs={'class': 'form-control', 'min': 0, 'step': 0.25}),
    }


class BodyMeasurementForm(forms.ModelForm):
    class Meta:
        model = BodyMeasurement
        fields = ["date", "weight", "chest", "waist", "hips", "arms", "legs"]
        labels = {
            "date": "Data pomiaru",
            "weight": "Waga (kg)",
            "chest": "Obwód klatki piersiowej (cm)",
            "waist": "Obwód talii (cm)",
            "hips": "Obwód bioder (cm)",
            "arms": "Obwód ręki (cm)",
            "legs": "Obwód uda (cm)",
        }
        widgets ={
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "weight": forms.NumberInput(attrs={"class": "form-control", "min": "0", "step": "0.01"}),
            "chest": forms.NumberInput(attrs={"class": "form-control", "min": "0", "step": "0.1"}),
            "waist": forms.NumberInput(attrs={"class": "form-control", "min": "0", "step": "0.1"}),
            "hips": forms.NumberInput(attrs={"class": "form-control", "min": "0", "step": "0.1"}),
            "arms": forms.NumberInput(attrs={"class": "form-control", "min": "0", "step": "0.1"}),
            "legs": forms.NumberInput(attrs={"class": "form-control", "min": "0", "step": "0.1"}),
        }

    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date and date > now().date():
            raise forms.ValidationError("Nie możesz dodać pomiaru z przyszłości!")
        return date

    def clean_weight(self):
        weight = self.cleaned_data.get("weight")
        if weight is None:
            raise forms.ValidationError("To pole jest wymagane!")
        if weight <= 0:
            raise forms.ValidationError("Waga musi być liczbą dodatnią!")
        return weight

    def clean_chest(self):
        chest = self.cleaned_data.get("chest")
        if chest is not None and chest <= 0:
            raise forms.ValidationError("Obwód klatki musi być liczbą dodatnią!")
        return chest

    def clean_waist(self):
        waist = self.cleaned_data.get("waist")
        if waist is not None and waist <= 0:
            raise forms.ValidationError("Obwód talii musi być liczbą dodatnią!")
        return waist

    def clean_hips(self):
        hips = self.cleaned_data.get("hips")
        if hips is not None and hips <= 0:
            raise forms.ValidationError("Obwód bioder musi być liczbą dodatnią!")
        return hips

    def clean_arms(self):
        arms = self.cleaned_data.get("arms")
        if arms is not None and arms <= 0:
            raise forms.ValidationError("Obwód ręki musi być liczbą dodatnią!")
        return arms

    def clean_thighs(self):
        thighs = self.cleaned_data.get("thighs")
        if thighs is not None and thighs <= 0:
            raise forms.ValidationError("Obwód uda musi być liczbą dodatnią!")
        return thighs
