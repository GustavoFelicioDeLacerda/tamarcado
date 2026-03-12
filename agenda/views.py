# agenda/views.py
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import Agendamento
from .serializers import AgendamentoSerializer
from datetime import timedelta
import re

# LISTAR AGENDAMENTOS (não mostra cancelados)
@api_view(['GET'])
def listar_agendamentos(request):
    agendamentos = Agendamento.objects.filter(cancelado=False)
    serializer = AgendamentoSerializer(agendamentos, many=True)
    return Response(serializer.data)


# DETALHAR UM AGENDAMENTO
@api_view(['GET'])
def detalhar_agendamento(request, id):
    try:
        agendamento = Agendamento.objects.get(id=id, cancelado=False)
    except Agendamento.DoesNotExist:
        return Response({'erro': 'Agendamento não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    serializer = AgendamentoSerializer(agendamento)
    return Response(serializer.data)


# CRIAR AGENDAMENTO
@api_view(['POST'])
def criar_agendamento(request):
    serializer = AgendamentoSerializer(data=request.data)
    if serializer.is_valid():
        data_horario = serializer.validated_data['data_horario']
        email = serializer.validated_data['email_cliente']
        telefone = serializer.validated_data['telefone_cliente']

        # Validação telefone
        if not re.fullmatch(r'\+?\d[\d\-\(\)]{7,}', telefone):
            return Response(
                {'erro': 'Telefone inválido. Deve ter no mínimo 8 dígitos e formato válido.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar duplicidade por email no mesmo dia
        if Agendamento.objects.filter(
            email_cliente=email,
            data_horario__date=data_horario.date(),
            cancelado=False
        ).exists():
            return Response(
                {'erro': 'Já existe um agendamento para este email nesta data.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Verificar intervalo de 30 minutos
        delta = timedelta(minutes=30)
        inicio = data_horario - delta
        fim = data_horario + delta
        if Agendamento.objects.filter(
            data_horario__range=(inicio, fim),
            cancelado=False
        ).exists():
            return Response(
                {'erro': 'Já existe um agendamento próximo a esse horário (intervalo de 30 minutos).'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# CANCELAR AGENDAMENTO (não excluir)
@api_view(['PATCH'])
def cancelar_agendamento(request, id):
    try:
        agendamento = Agendamento.objects.get(id=id)
    except Agendamento.DoesNotExist:
        return Response({'erro': 'Agendamento não encontrado'}, status=status.HTTP_404_NOT_FOUND)
    
    agendamento.cancelado = True
    agendamento.save()
    return Response({'sucesso': 'Agendamento cancelado'}, status=status.HTTP_200_OK)