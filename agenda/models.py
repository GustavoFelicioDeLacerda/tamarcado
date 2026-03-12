from django.db import models

class Agendamento(models.Model):
    nome_cliente = models.CharField(max_length=100)
    email_cliente = models.EmailField()
    telefone_cliente = models.CharField(max_length=20)
    data_horario = models.DateTimeField()
    cancelado = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.nome_cliente} - {self.data_horario}"