import json
import pandas as pd

with open("db.json", "r") as f:
    db = json.load(f)

df = pd.DataFrame()
df['HASH'] = ""
df['CATEGORIA'] = ""
df['NOME'] = ""
df['TIPO'] = ""
df['PRECO'] = 0

for category in db:
    for product in db[category]:
        if not db[category][product]:
            print(f"[ERRO] Produto inexistente {product}")
            continue
        hash = db[category][product]["hash"]
        if not hash:
            print(f"[NOTE] Produto indisponivel {product}")
            continue
        nome = db[category][product]["nome"].replace("\n", "")
        try:
            preco = float(db[category][product]["preco"].split('$')[1].replace(',', '.'))
        except IndexError:
            preco = float(db[category][product]["preco"])
        if preco == 0:
            print(f"[ERRO] Produto sem preco {product}")
            continue
        if not db[category][product]["opcoes"]:
            row = [hash, category, nome, '-', preco]
            df.loc[len(df.index)] = row
        else:
            for opcao in db[category][product]["opcoes"]:
                if db[category][product]["opcoes"][opcao] == "0":
                    continue
                hash = hash.split('-')
                hash[1] = db[category][product]["opcoes"][opcao]
                hash = '-'.join(hash)
                row = [hash, category, nome, opcao, preco]
                df.loc[len(df.index)] = row

print(df)
df.to_csv("produtos.csv")

