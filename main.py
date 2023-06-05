import config
import logging
from enum import Enum
from telegram import Update
from telegram import ReplyKeyboardMarkup, KeyboardButton
from telegram import InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler, CallbackQueryHandler

# constantes
OPERACAO_VOLTAR = -1
OPERACAO_CANCELAR = 0
OPERACAO_CONFIRMAR = 1

# mensagens globais
msg_cancelar = '🚫 sair'
msg_confirmar = '✅ confirmar'
msg_voltar = '🔙 voltar'

class Menu(Enum):
    INICIAR_PEDIDO = 1
    ADICIONAR_PRODUTO = 2
    REMOVER_PRODUTO = 3
    EXIBIR_CARRINHO = 4
    FINALIZAR_PEDIDO = 5


# habilita logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)



async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    chat_id = update.message.chat_id
    username = user.username
    first_name = user.first_name
    last_name = user.last_name

    print(f"ID do usuário: {chat_id}")
    print(f"Usernaxme: {username}")
    print(f"Nome completo: {first_name} {last_name}")

    msg = f'''Olá chatid {chat_id} \n
    {first_name} {last_name} você me convocaste seu seboso?.\n\n
    Me chamo testobot, o bot da TESTOSTERONA ALTA, fui criado por motivos de incopetencia de alguns integrantes da computacao e
    a partir de hoje eu serei o vosso mentor, o mais sábio, o mais poderoso, o pai de todos: O DUNGEON KING\n\n
    Ainda estou em fase de implementação rs, porém em breve estarei preparado para lidar com todas atrocidades que me forem atribuidas.\n
    Não sei mais o que falar porque nao me tornei um ser pensante (ainda) mas o que posso adiantar é que serei a maior criação que a URGUES será capaz de presenciar.\n
    Estou na versao 0.00069 mas espero algum dia ser comercializado para ganhar muinto dinheiro.\n\n
    Até logo xD'''

    await context.bot.send_message(chat_id=chat_id, text=msg)


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = f'msg de ajuda /comandos'
    await context.bot.send_message(chat_id=update.message.chat_id, text=msg)
    
    #mensagem usando reply
    #await update.effective_message.reply_text(msg)
    
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['authorized_user_id'] = update.message.from_user.id
    
    msg = 'escolha funcionalidade: '
    
    botoes = [
        [InlineKeyboardButton('iniciar pedido', callback_data=Menu.INICIAR_PEDIDO.value)],
        [InlineKeyboardButton('exibir pedido atual', callback_data=Menu.ADICIONAR_PRODUTO.value)],
        [InlineKeyboardButton('adicionar produto(s)', callback_data= Menu.REMOVER_PRODUTO.value)],
        [InlineKeyboardButton('cancelar produto(s)', callback_data=Menu.EXIBIR_CARRINHO.value)],
        [InlineKeyboardButton('finalizar pedido', callback_data=Menu.FINALIZAR_PEDIDO.value)],
        [InlineKeyboardButton(msg_cancelar, callback_data=OPERACAO_CANCELAR)],
    ]
    

    reply_markup = InlineKeyboardMarkup(botoes)
    
    await context.bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=reply_markup)
    
async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query

    if query.from_user.id == context.user_data.get('authorized_user_id'):
        await query.edit_message_text(text=f'opcao selecionada {query.data}')
        
        #TODO add functionalities
        if query.data == Menu.INICIAR_PEDIDO.value:
            pass
        elif query.data == Menu.ADICIONAR_PRODUTO.value:
            pass
        elif query.data == Menu.REMOVER_PRODUTO.value:
            pass
        elif query.data == Menu.EXIBIR_CARRINHO.value:
            pass
        elif query.data == Menu.FINALIZAR_PEDIDO.value:
            pass
        elif query.data == OPERACAO_CANCELAR:
            pass
    else:
        await query.answer(text=f'{query.from_user.first_name}, não foi você que chamou o menu!', show_alert=True)



def main():
    application = ApplicationBuilder().token(config.TOKEN).build()
    
    application.add_handler(CommandHandler('start', start_handler))
    application.add_handler(CommandHandler('help', help_handler))

    application.add_handler(CommandHandler('menu', menu_handler))
    application.add_handler(CallbackQueryHandler(menu_callback))

    
    application.run_polling()


if __name__ == '__main__':
    main()

