from django.contrib.auth.views import LogoutView
from django.urls import path
from django.contrib.auth import views as auth_views
from django.views.decorators.csrf import csrf_exempt

from .views import dashboard, register, add_workout, add_body_measurement, progress, training_plans, \
    edit_training_plan, delete_training_plan, add_exercise, define_training_plan, add_exercise_to_workout, \
    add_exercise_to_day, create_training_plan, edit_exercise, delete_exercise, add_exercise_to_plan, get_exercises, \
    workout_history, bmi_calculator, tdee_calculator, edit_workout, delete_workout, update_measurement, set_csrf_cookie

urlpatterns = [
    path('', dashboard, name='dashboard'),
    path('register/', register, name='register'),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path("set-csrf-cookie/", set_csrf_cookie, name="set_csrf_cookie"),

    path('dodaj_plan/', create_training_plan, name='create_training_plan'),
    path('zdefiniuj_cwiczenia/', define_training_plan, name='define_training_plan'),
    path('dodaj_cwiczenie_dzien/<int:day_id>/', add_exercise_to_day, name='add_exercise_to_day'),
    path('plany_treningowe/', training_plans, name='training_plans'),
    path('plany_treningowe/dodaj_plan/', training_plans, name='training_plans'),
    path('zdefiniuj_plan/<int:plan_id>/', define_training_plan, name='define_training_plan'),
    path('dodaj_cwiczenie/<int:day_id>/', add_exercise, name='add_exercise'),
    path("edytuj_plan/<int:plan_id>/", edit_training_plan, name="edit_training_plan"),
    path("edytuj_cwiczenie/<int:exercise_id>/", edit_exercise, name="edit_exercise"),
    path("usun_cwiczenie/<int:exercise_id>/", delete_exercise, name="delete_exercise"),
    path("usun_plan/<int:plan_id>/", delete_training_plan, name="delete_training_plan"),
    path("dodaj_cwiczenie_do_planu/<int:plan_id>/", add_exercise_to_plan, name="add_exercise_to_plan"),
    path("dodaj_trening/", add_workout, name="add_workout"),
    path("get_exercises/<int:day_id>/", get_exercises, name="get_exercises"),
    path('dodaj_cwiczenie/<int:workout_id>/<int:day_number>/', add_exercise_to_workout, name='add_exercise_to_workout'),
    path("historia_treningow/", workout_history, name="workout_history"),
    path("historia_treningow/edytuj_trening/<int:workout_id>/", edit_workout, name="edit_workout"),
    path("historia_treningow/usun_trening/<int:workout_id>/", delete_workout, name="delete_workout"),
    path("pomiary/", progress, name="progress"),
    path("pomiary/dodaj/", add_body_measurement, name="add_body_measurement"),
    path("pomiary/bmi/", bmi_calculator, name="bmi_calculator"),
    path("pomiary/tdee/", tdee_calculator, name="tdee_calculator"),
    path("update-measurement/", update_measurement, name="update_measurement"),

]
