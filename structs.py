import pandas as pd

# colunas dfs

# df_pedidos -> pedidos.csv
# id | compradores | produtos

# df_produtos -> produtos.csv
# id | hash | categoria | nome | tipo | preco  

class Pedido:
    def __init__(self, df_pedidos) -> None:
        df_pedidos = df_pedidos.append({})
        self.id = df_pedidos.index.max()
        self.compradores = []
        self.produtos = []
        
    def add_produto(produto) -> None:
        pass

    

    def finalizar_compra() -> None:
        pass

class Comprador:
    def __init__(self, id) -> None:
        self.id = id
        self.produtos = []
    

