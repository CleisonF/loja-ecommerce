def formata_preco(preco):
    return f'R$ {preco:.2f}'.replace('.', ',')

def cart_total_qtd(carrinho):
    total_qtd = sum(item['quantidade'] for item in carrinho.values())
    return total_qtd

def cart_total_valor(carrinho):
    return sum(
        [
            item.get('preco_quantitativo_promocional')
            if item.get('preco_quantitativo_promocional') 
            else item.get('preco_quantitativo')
            for item in carrinho.values()
        ]
    )
