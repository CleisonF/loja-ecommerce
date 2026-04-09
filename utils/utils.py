def formata_preco(preco):
    return f'R$ {preco:.2f}'.replace('.', ',')

def cart_total_qtd(carrinho):
    total_qtd = sum(item['quantidade'] for item in carrinho.values())
    return total_qtd

def cart_total_valor(carrinho):
    total_valor = sum(item['quantidade'] * item['preco_unitario'] for item in carrinho.values())
    return total_valor