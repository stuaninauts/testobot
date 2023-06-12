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
        
    def add_produto(self, produto, comprador_id) -> None:
        if comprador_id not in self.compradores:
            comprador = Comprador(comprador_id)
            self.compradores.append(comprador)
        
        comprador.produtos.append(produto)

    def rm_produto(self, produto, comprador) -> None:
        comprador.produtos.remove(produto)
        if not comprador.produtos:
            self.compradores.remove(comprador)

    def print(self) -> None:
        pass

    def finalizar_pedido() -> None:
        pass

class Comprador:
    def __init__(self, id) -> None:
        self.id = id
        self.produtos = []
    

