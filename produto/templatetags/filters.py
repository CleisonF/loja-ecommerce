from django.template import Library
from utils.utils import (
    formata_preco, cart_total_qtd as cart_total_qtd_utils,
    cart_total_valor as cart_total_valor_utils
)

register = Library()


@register.filter(name='formatar_preco')
def formatar_preco_filter(value):
    return formata_preco(value)

@register.filter(name='cart_total_qtd')
def cart_total_qtd_filter(carrinho):
    return cart_total_qtd_utils(carrinho)

@register.filter(name='cart_total_valor')
def cart_total_valor_filter(carrinho):
    return cart_total_valor_utils(carrinho)
