from django.template import Library
from utils.utils import formata_preco

register = Library()


@register.filter(name='formatar_preco')
def formatar_preco(value):
    return formata_preco(value)

@register.filter(name='cart_total_qtd')
def cart_total_qtd(carrinho):
    return (cart_total_qtd(carrinho))

@register.filter(name='cart_total_valor')
def cart_total_valor(carrinho):
    return formata_preco(cart_total_valor(carrinho))
