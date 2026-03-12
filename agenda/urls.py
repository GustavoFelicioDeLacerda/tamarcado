from django.urls import path
from . import views

urlpatterns = [
    path('agendamentos/', views.listar_agendamentos),
    path('agendamentos/<int:id>/', views.detalhar_agendamento),
    path('agendamentos/criar/', views.criar_agendamento),
    path('agendamentos/<int:id>/cancelar/', views.cancelar_agendamento),
]