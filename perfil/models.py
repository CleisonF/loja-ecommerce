from django.db import models
from django.contrib.auth.models import User

import re

from django.forms import ValidationError
from utils.validacpf import valida_cpf

class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    idade = models.IntegerField(null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    cpf = models.CharField(max_length=14, null=True, blank=True)
    endereco = models.CharField(max_length=255, null=True, blank=True)
    numero = models.CharField(max_length=5, null=True, blank=True)
    complemento = models.CharField(max_length=30, null=True, blank=True)
    bairro = models.CharField(max_length=30, null=True, blank=True)
    cep = models.CharField(max_length=8, null=True, blank=True)
    cidade = models.CharField(max_length=30, null=True, blank=True)
    estado = models.CharField(
        max_length=2,
        choices=(
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins')
        )
    )

    def __str__(self):
        return f'{self.usuario}'

    def clean(self):
        error_messages = {}
        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'CPF inválido.'

        if re.search(r'[^0-9]', self.cep) or len(self.cep) != 8:
            error_messages['cep'] = 'O campo CEP deve conter apenas dígitos e ter 8 caracteres.'    

        if error_messages:
            raise ValidationError(error_messages)
        
        
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'
    
# Create your models here.
