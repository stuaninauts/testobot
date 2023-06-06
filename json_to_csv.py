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
            continue
        hash = db[category][product]["hash"]
        if hash == "00":
            print(f"{product} indisponivel")
            continue
        nome = db[category][product]["nome"]
        try:
            preco = float(db[category][product]["preco"].split('$')[1].replace(',', '.'))
        except:
            preco = float(db[category][product]["preco"])
        if not db[category][product]["opcoes"]:
            row = [hash, category, nome, '-', preco]
            df.loc[len(df.index)] = row
        else:
            for opcao in db[category][product]["opcoes"]:
                if opcao == "Escolha o Sabor":
                    continue
                hash = hash.split('-')
                hash[1] = db[category][product]["opcoes"][opcao]
                hash = '-'.join(hash)
                row = [hash, category, nome, opcao, preco]
                df.loc[len(df.index)] = row

print(df)
df.to_csv("produtos.csv")

