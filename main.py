import config
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from selenium import webdriver
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler




async def teste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    chat_id = update.message.chat_id
    username = user.username
    first_name = user.first_name
    last_name = user.last_name

    print(f"ID do usuário: {chat_id}")
    print(f"ID do usuário: {username}")
    print(f"Nome completo: {first_name} {last_name}")

    mensagem = f'''Olá chatid {chat_id} \n
    {first_name} {last_name} você me convocaste seu seboso?.\n\n
    Me chamo testobot, o bot da TESTOSTERONA ALTA, fui criado por motivos de incopetencia de alguns integrantes da computacao e
    a partir de hoje eu serei o vosso mentor, o mais sábio, o mais poderoso, o pai de todos: O DUNGEON KING\n\n
    Ainda estou em fase de implementação rs, porém em breve estarei preparado para lidar com todas atrocidades que me forem atribuidas.\n
    Não sei mais o que falar porque nao me tornei um ser pensante (ainda) mas o que posso adiantar é que serei a maior criação que a URGUES será capaz de presenciar.\n
    Estou na versao 0.00069 mas espero algum dia ser comercializado para ganhar muinto dinheiro.\n\n
    Até logo xD'''


    await context.bot.send_message(chat_id=chat_id, text=mensagem)



# dado um link, adiciona o link no carrinho
def add_carrinho(update, context):
    link = context.args[0]

    # logica fuckeeers

    #TODO talvez implementar classe pedido e fazer todas bagaça

    produto = extrai_nome_produto(link)
    sabores = extrai_sabores(link)

    # se produto nao tem sabor:
    context.bot.send_message(chat_id=update.effective_chat.id, text=f'Produto {produto} adicionado ao carrinho!')
    
    # se produto tem sabor:
    # TODO listar opcoes disponiveis e indisponiveis e perguntar ao usuario a escolha

    





# dado um link, extrai o nome do produto contido na URL
def extrai_nome_produto(link):
    parsed_url = urlparse(link)
    produto = parsed_url.path[1:]

    #TODO tratar o url pós .br/ ...

    return produto


# dado um link, retorna um dicionario com os sabores disponiveis e nao disponiveis
def extrai_sabores(link):

    sabores = {
        'sabor': None, 
        'disponivel': False
    }


    #TODO 
    # extrair info do site
    # excluir primeiro elem (Escolha sabor)
    # separar disponiveis e indisponiveis 
    html = '<ul class="list"><li data-value="0" class="option selected">Escolha o Sabor</li><li data-value="1" class="option">Chocolate</li>'
    
    soup = BeautifulSoup(html, 'html.parser')

    itens = soup.find_all(class_="option")

    sabores = [item.get_text() for item in itens]


    return sabores


# dado um comprador e o pix, cria um pix copia e cola para o pagamento de cada um ser feito
def finalizar_compra(pedido, pix):
    #TODO tudo kkkk
    return




def main():
    application = ApplicationBuilder().token(config.TOKEN).build()
    
    testando = CommandHandler('teste', teste)
    application.add_handler(testando)
    
    application.run_polling()


if __name__ == '__main__':
    main()

