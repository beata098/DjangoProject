import json
import random
from datetime import timedelta, date, datetime

from django.core.checks import messages
from django.http import JsonResponse
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from .forms import RegisterForm, BodyMeasurementForm, TrainingPlanForm, ExerciseForm
from .models import Workout, WorkoutExercise, TrainingPlan, TrainingDay, Exercise, BodyMeasurement
from django.shortcuts import redirect, get_object_or_404, render
from django.utils.timezone import now


MOTIVATION_QUOTES = [
    "Nie poddawaj się! Sukces to suma małych wysiłków powtarzanych każdego dnia.",
    "Każdy trening przybliża Cię do celu!",
    "Twoje ciało może wytrzymać więcej, niż podpowiada Ci umysł.",
    "Nie czekaj. Czas nigdy nie będzie idealny.",
    "Dzisiaj robisz to, czego inni nie chcą, a jutro osiągniesz to, czego inni nie mogą.",
    "Siła nie pochodzi z wygrywania. Twoje zmagania rozwijają Twoją siłę.",
    "Nie liczy się to, ile razy upadniesz, ale ile razy wstaniesz.",
    "Ból jest tymczasowy, duma trwa wiecznie!",
    "Zacznij tam, gdzie jesteś. Użyj tego, co masz. Zrób to, co możesz.",
    "Twój jedyny limit to ten, który sobie narzucasz."
]


@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            login(request, user)  # Automatyczne logowanie po rejestracji
            return redirect('dashboard')
    else:
        form = RegisterForm()

    return render(request, 'tracker/register.html', {'form': form})

@login_required
def dashboard(request):
    username = request.user.username
    random_quote = random.choice(MOTIVATION_QUOTES)

    recent_workouts = Workout.objects.filter(
        user=request.user,
        date__gte=now() - timedelta(days=7),
        date__lte=now().date()
    ).order_by('date')
    user_exercises = WorkoutExercise.objects.filter(workout__user=request.user).values_list('name', flat=True).distinct()


    selected_exercise = request.GET.get("exercise")
    chart_labels = []
    chart_data = []

    if selected_exercise:
        history = (
            WorkoutExercise.objects
            .filter(workout__user=request.user, name=selected_exercise)
            .values("workout__date", "ciezar")
            .order_by("workout__date")
        )

        chart_labels = [entry["workout__date"].strftime("%d-%m-%Y") for entry in history]
        chart_data = [entry["ciezar"] for entry in history]

    return render(request, "tracker/dashboard.html", {
        "username": username,
        "quote": random_quote,
        "recent_workouts": recent_workouts,
        "user_exercises": user_exercises,
        "selected_exercise": selected_exercise,
        "chart_labels": json.dumps(chart_labels),
        "chart_data": json.dumps(chart_data),
    })

@login_required
def create_training_plan(request):
    if request.method == 'POST':
        form = TrainingPlanForm(request.POST)
        if form.is_valid():
            # Tworzymy plan, ale jeszcze go nie zapisujemy
            plan = form.save(commit=False)
            plan.user = request.user
            plan.save()

            for i in range(1, plan.days_per_week + 1):
                TrainingDay.objects.create(plan=plan, day_number=i)
            return redirect('define_training_plan', plan_id=plan.id)

    else:
        form = TrainingPlanForm()

    return render(request, 'tracker/create_training_plan.html', {'form': form})


@login_required
def define_training_plan(request, plan_id):
    plan = get_object_or_404(TrainingPlan, id=plan_id)
    training_days = plan.training_days.all()

    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            training_day_id = request.POST.get('training_day')  # Pobieramy dzień treningowy z formularza
            training_day = get_object_or_404(TrainingDay, id=training_day_id)
            exercise = form.save(commit=False)
            exercise.training_day = training_day  # Przypisujemy ćwiczenie do wybranego dnia
            exercise.save()
            return redirect('define_training_plan', plan_id=plan.id)  # Wracamy do tej samej strony, aby dodać więcej ćwiczeń

    form = ExerciseForm()
    return render(request, 'tracker/define_training_plan.html', {'form': form, 'plan': plan, 'training_days': training_days})


@login_required
def training_plans(request):
    plans = TrainingPlan.objects.filter(user=request.user)
    return render(request, 'tracker/training_plans.html', {'plans': plans})


# @login_required
# def add_training_plan(request):
#     if request.method == 'POST':
#         form = TrainingPlanForm(request.POST)
#         if form.is_valid():
#             plan = form.save(commit=False)
#             plan.user = request.user
#             plan.save()
#
#             # Automatyczne tworzenie dni treningowych
#             for day_number in range(1, plan.days_per_week + 1):
#                 TrainingDay.objects.create(plan=plan, day_number=day_number)
#
#             return redirect('define_training_plan', plan_id=plan.id)
#     else:
#         form = TrainingPlanForm()
#     return render(request, 'tracker/add_training_plan.html', {'form': form})

@login_required
def add_exercise_to_day(request, day_id):
    day = get_object_or_404(TrainingDay, id=day_id, plan__user=request.user)
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.training_day = day
            exercise.save()
            return redirect('define_training_plan', plan_id=day.plan.id)  # Wracamy do listy dni
    else:
        form = ExerciseForm()
    return render(request, 'tracker/add_exercise.html', {'form': form, 'day': day})

@login_required
def add_exercise(request, day_id):
    day = get_object_or_404(TrainingDay, id=day_id, plan__user=request.user)
    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.day = day
            exercise.save()
            return redirect('define_training_plan', plan_id=day.plan.id)
    else:
        form = ExerciseForm()
    return render(request, 'tracker/add_exercise.html', {'form': form, 'day': day})


@login_required
def edit_training_plan(request, plan_id):
    plan = get_object_or_404(TrainingPlan, id=plan_id)
    exercises = Exercise.objects.filter(training_day__plan=plan)  # Pobierz ćwiczenia przypisane do planu

    if request.method == "POST":
        form = TrainingPlanForm(request.POST, instance=plan)
        if form.is_valid():
            form.save()
            return redirect("training_plans")  # Po edycji wracamy do listy planów
    else:
        form = TrainingPlanForm(instance=plan)

    return render(request, "tracker/edit_training_plan.html", {
        "form": form,
        "plan": plan,
        "exercises": exercises,
    })

@login_required
def delete_training_plan(request, plan_id):
    plan = get_object_or_404(TrainingPlan, id=plan_id)
    plan.delete()
    return redirect("training_plans")  # Przekierowanie do listy planów


@login_required
def add_workout(request):
    training_plans = TrainingPlan.objects.filter(user=request.user)

    if not training_plans.exists():
        return render(request, "tracker/add_workout.html", {
            "training_plans": None,
            "training_days": None,
            "error": "Nie masz jeszcze żadnych planów treningowych. Dodaj plan, aby kontynuować."
        })

    selected_plan_id = request.GET.get("plan")
    selected_day_id = request.GET.get("day")
    selected_plan = None
    selected_day = None
    training_days = None
    exercises = None

    if selected_plan_id:
        selected_plan = get_object_or_404(TrainingPlan, id=selected_plan_id, user=request.user)
        training_days = TrainingDay.objects.filter(plan=selected_plan).order_by("day_number")

    if selected_day_id and selected_plan:
        selected_day = get_object_or_404(TrainingDay, id=selected_day_id, plan=selected_plan)
        exercises = Exercise.objects.filter(training_day=selected_day)

    if request.method == "POST":
        plan_id = request.POST.get("plan")
        day_id = request.POST.get("day")

        if not plan_id or not day_id:
            return render(request, "tracker/add_workout.html", {
                "training_plans": training_plans,
                "training_days": training_days,
                "error": "Musisz wybrać plan treningowy i dzień treningowy!"
            })

        plan = get_object_or_404(TrainingPlan, id=plan_id, user=request.user)
        day = get_object_or_404(TrainingDay, id=day_id, plan=plan)
        workout_date = request.POST.get("date")
        workout = Workout.objects.create(user=request.user, training_day=day, date=workout_date)
        exercises = Exercise.objects.filter(training_day=day)

        for exercise in exercises:
            weight = request.POST.get(f"weight_{exercise.id}", 0)
            WorkoutExercise.objects.create(
                workout=workout,
                exercise=exercise,
                name=exercise.nazwa,
                serie=exercise.serie,
                powtorzenia=exercise.powtorzenia,
                ciezar=weight
            )

        return redirect("dashboard")

    return render(request, "tracker/add_workout.html", {
        "training_plans": training_plans,
        "training_days": training_days,
        "selected_plan": selected_plan,
        "selected_day": selected_day,
        "exercises": exercises
    })

@login_required
def add_exercise_to_workout(request, workout_id, day_number=1):
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)

    # Sprawdź, czy istnieje "TrainingDay" dla tego treningu i dnia
    training_day = TrainingDay.objects.get(plan_id=workout_id, day_number=day_number)

    if request.method == 'POST':
        form = ExerciseForm(request.POST)
        if form.is_valid():
            exercise = form.save(commit=False)
            exercise.training_day = training_day
            exercise.save()
            return redirect('add_exercise_to_workout', workout_id=workout.id, day_number=day_number)
    else:
        form = ExerciseForm()

    return render(request, 'tracker/add_exercise.html', {
        'form': form,
        'workout': workout,
        'training_day': training_day
    })

# @login_required
# def add_training_plan(request):
#     if request.method == 'POST':
#         form = TrainingPlanForm(request.POST)
#         if form.is_valid():
#             plan = form.save(commit=False)
#             plan.user = request.user
#             plan.save()
#             return redirect('training_plans')
#     else:
#         form = TrainingPlanForm()
#     return render(request, 'tracker/add_training_plan.html', {'form': form})

@login_required
def edit_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)

    if request.method == "POST":
        form = ExerciseForm(request.POST, instance=exercise)
        if form.is_valid():
            form.save()
            return redirect("edit_training_plan", plan_id=exercise.training_day.plan.id)  # ⬅️ Powrót do edycji planu
    else:
        form = ExerciseForm(instance=exercise)

    return render(request, "tracker/edit_exercise.html", {"form": form, "exercise": exercise})

@login_required
def delete_exercise(request, exercise_id):
    exercise = get_object_or_404(Exercise, id=exercise_id)
    plan_id = exercise.training_day.plan.id
    exercise.delete()
    return redirect("edit_training_plan", plan_id=plan_id)


@login_required
def add_exercise_to_plan(request, plan_id):
    plan = get_object_or_404(TrainingPlan, id=plan_id)
    training_days = plan.training_days.all()  # Pobieramy dni treningowe dla planu

    if request.method == "POST":
        form = ExerciseForm(request.POST)
        if form.is_valid():
            training_day_id = request.POST.get("training_day")
            training_day = get_object_or_404(TrainingDay, id=training_day_id)

            exercise = form.save(commit=False)
            exercise.training_day = training_day  # Przypisujemy ćwiczenie do dnia treningowego
            exercise.save()
            return redirect("edit_training_plan", plan_id=plan.id)  # Powrót do edycji planu
    else:
        form = ExerciseForm()

    return render(request, "tracker/add_exercise_to_plan.html", {
        "form": form,
        "plan": plan,
        "training_days": training_days,
    })

@login_required
def get_exercises(request, day_id):
    training_day = get_object_or_404(TrainingDay, id=day_id)
    exercises = Exercise.objects.filter(training_day=training_day)

    exercises_list = [{
        "id": ex.id,
        "nazwa": ex.nazwa,
        "serie": ex.serie,
        "powtorzenia": ex.powtorzenia
    } for ex in exercises]

    return JsonResponse(exercises_list, safe=False)

@login_required
def workout_history(request):
    workouts = Workout.objects.filter(user=request.user).order_by("-date").select_related("training_day", "plan")
    return render(request, "tracker/workout_history.html", {"workouts": workouts})

@login_required
def edit_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)

    if request.method == "POST":
        date = request.POST.get("date")
        workout.date = date
        workout.save()

        # Edycja ćwiczeń (jeśli użytkownik coś zmienił)
        for exercise in workout.exercises.all():
            weight = request.POST.get(f"weight_{exercise.id}")
            if weight is not None:
                exercise.ciezar = weight
                exercise.save()

        return redirect("workout_history")

    return render(request, "tracker/edit_workout.html", {
        "workout": workout,
        "exercises": workout.exercises.all()
    })


@login_required
def delete_workout(request, workout_id):
    workout = get_object_or_404(Workout, id=workout_id, user=request.user)

    if request.method == "POST":
        workout.delete()
        return redirect("workout_history")

    return render(request, "tracker/delete_workout.html", {"workout": workout})

@login_required
def progress(request):
    measurements = BodyMeasurement.objects.filter(user=request.user).order_by("date")

    context = {
        "measurements": measurements,
        "dates": json.dumps([m.date.strftime("%Y-%m-%d") for m in measurements]),  # Konwersja dat na JSON
        "weights": json.dumps([m.weight for m in measurements]),
        "chest": json.dumps([m.chest or None for m in measurements]),
        "waist": json.dumps([m.waist or None for m in measurements]),
        "hips": json.dumps([m.hips or None for m in measurements]),
        "arms": json.dumps([m.arms or None for m in measurements]),
        "legs": json.dumps([m.legs or None for m in measurements]),
        "timestamp": datetime.now().timestamp(),
    }

    return render(request, "tracker/progress.html", context)

# @login_required
# def progress(request):
#     measurements = BodyMeasurement.objects.filter(user=request.user).order_by("date")
#
#     dates = [m.date.strftime("%d-%m-%Y") for m in measurements]
#     weights = [m.weight for m in measurements]
#     chest = [m.chest if m.chest is not None else None for m in measurements]
#     waist = [m.waist if m.waist is not None else None for m in measurements]
#     hips = [m.hips if m.hips is not None else None for m in measurements]
#     arms = [m.arms if m.arms is not None else None for m in measurements]
#     legs = [m.legs if m.legs is not None else None for m in measurements]
#
#     return render(request, "tracker/progress.html", {
#         "measurements": measurements,
#         "dates": json.dumps(dates),
#         "weights": json.dumps(weights),
#         "chest": json.dumps(chest),
#         "waist": json.dumps(waist),
#         "hips": json.dumps(hips),
#         "arms": json.dumps(arms),
#         "legs": json.dumps(legs)
#     })


@login_required
def add_body_measurement(request):
    if request.method == "POST":
        form = BodyMeasurementForm(request.POST)
        if form.is_valid():
            measurement = form.save(commit=False)
            measurement.user = request.user
            measurement.save()
            return redirect("progress")
    else:
        form = BodyMeasurementForm()

    return render(request, "tracker/add_body_measurement.html", {"form": form})


@login_required
def update_measurement(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            measurement_id = data.get("id")
            field = data.get("field")
            value = data.get("value").strip()


            measurement = BodyMeasurement.objects.get(id=measurement_id)


            if value == "":
                value = None
            elif field in ["weight", "chest", "waist", "hips", "arms", "legs"]:
                try:
                    value = float(value)
                except ValueError:
                    return JsonResponse({"success": False, "error": f"Niepoprawna wartość dla {field}"}, status=400)

                # Sprawdzenie, czy wartość jest >= 0
                if value < 0:
                    return JsonResponse({"success": False, "error": f"Wartość dla {field} nie może być mniejsza niż 0"}, status=400)

            # Aktualizacja wartości
            setattr(measurement, field, value)
            measurement.save()

            return JsonResponse({"success": True})

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)

    return JsonResponse({"success": False, "error": "Nieprawidłowe żądanie"}, status=400)

@login_required
def delete_measurement(request, measurement_id):
    measurement = get_object_or_404(BodyMeasurement, id=measurement_id, user=request.user)
    measurement.delete()
    return redirect('progress')  # Przekierowanie z powrotem do historii pomiarów


# @csrf_exempt  # Jeśli używasz standardowego Django CSRF, zamień to na @require_http_methods(["PATCH"])
# def update_measurement(request):
#     if request.method == "PATCH":
#         try:
#             # Parsowanie danych JSON
#             data = json.loads(request.body)
#             measurement_id = data.get("id")
#             field = data.get("field")
#             value = data.get("value")
#
#             # Walidacja ID i pola
#             if not measurement_id or not field:
#                 return JsonResponse({"success": False, "error": "Brak wymaganych danych"}, status=400)
#
#             # Pobranie obiektu z bazy danych
#             measurement = BodyMeasurement.objects.get(id=measurement_id)
#
#             # Sprawdzenie poprawności typu wartości i konwersja na float
#             if value:
#                 try:
#                     value = float(value)
#                 except ValueError:
#                     return JsonResponse({"success": False, "error": "Nieprawidłowy format liczby"}, status=400)
#
#             # Aktualizacja rekordu w bazie
#             setattr(measurement, field, value)
#             measurement.save()  # Kluczowy moment - zapis zmian w bazie!
#
#             return JsonResponse({"success": True, "new_value": value})
#
#         except BodyMeasurement.DoesNotExist:
#             return JsonResponse({"success": False, "error": "Nie znaleziono pomiaru"}, status=404)
#         except Exception as e:
#             return JsonResponse({"success": False, "error": str(e)}, status=400)
#
#     return JsonResponse({"success": False, "error": "Nieprawidłowa metoda"}, status=405)

@login_required
def bmi_calculator(request):
    bmi = None
    category = None

    if request.method == "POST":
        weight = float(request.POST.get("weight", 0))
        height = float(request.POST.get("height", 0)) / 100  # cm -> m
        if height > 0:
            bmi = round(weight / (height * height), 2)
            if bmi < 18.5:
                category = "Niedowaga"
            elif 18.5 <= bmi < 24.9:
                category = "Prawidłowa waga"
            elif 25 <= bmi < 29.9:
                category = "Nadwaga"
            else:
                category = "Otyłość"

    return render(request, "tracker/bmi_calculator.html", {"bmi": bmi, "category": category})

@login_required
def tdee_calculator(request):
    tdee = None
    category = None

    if request.method == "POST":
        weight = float(request.POST.get("weight", 0))
        height = float(request.POST.get("height", 0))
        age = int(request.POST.get("age", 0))
        sex = request.POST.get("sex")
        activity_level = float(request.POST.get("activity_level", 1.2))

        if sex == "male":
            bmr = 88.36 + (13.4 * weight) + (4.8 * height) - (5.7 * age)
        else:
            bmr = 447.6 + (9.2 * weight) + (3.1 * height) - (4.3 * age)

        tdee = round(bmr * activity_level, 2)

    return render(request, "tracker/tdee_calculator.html", {"tdee": tdee})


