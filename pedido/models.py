from django.db import models
from django.contrib.auth.models import User



class Pedido(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.FloatField()
    status = models.CharField(
        default='C',
        max_length=1,
        choices=[
            ('A', 'Aprovado'),
            ('C', 'Criado'),
            ('R', 'Recusado'),
            ('P', 'Pendente'),
            ('E', 'Enviado'),
            ('F', 'Finalizado'),
        ]
    )

    def __str__(self):
        return f'Pedido N. {self.pk}'

class ItemPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.CharField(max_length=100)
    produto_id = models.PositiveIntegerField()
    variacao = models.CharField(max_length=100, blank=True, null=True)
    variacao_id = models.IntegerField(blank=True, null=True)
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0.0)
    quantidade = models.PositiveIntegerField(default=1)
    imagem = models.CharField(max_length=2000, blank=True, null=True)


    def __str__(self):
        return f'Item do {self.pedido}'
    
    class Meta:
        verbose_name = 'Item do Pedido'
        verbose_name_plural = 'Itens do Pedido'
        