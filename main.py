import config
import logging
import pandas as pd
from enum import Enum
from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
)

# constantes
OPERACAO_VOLTAR = -1
OPERACAO_CANCELAR = 0
OPERACAO_CONFIRMAR = 1

FLAG_PEDIDO = 0
# mensagens globais
msg_cancelar = '🚫 sair'
msg_confirmar = '✅ confirmar'
msg_voltar = '🔙 voltar'

#TODO create all buttons
# buttons = {
#     'iniciar_pedido'
# }

class Menu(Enum):
    INICIAR_PEDIDO, \
    EXIBIR_ANTERIORES, \
    ADICIONAR_PRODUTO, \
    REMOVER_PRODUTO, \
    EXIBIR_ATUAL, \
    FINALIZAR_PEDIDO = range(6)


# habilita logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
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


# async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
#     msg = f'msg de ajuda /comandos'
#     await context.bot.send_message(chat_id=update.message.chat_id, text=msg)
    
#     #mensagem usando reply
#     await update.effective_message.reply_text(msg)
    
async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    context.user_data['authorized_user_id'] = update.message.from_user.id
    
    msg = 'escolha funcionalidade: '
    
    #TODO handle the paths
    if FLAG_PEDIDO == 1:
        botoes = [           
            [InlineKeyboardButton('adicionar produto(s)', callback_data=Menu.ADICIONAR_PRODUTO.value)],
            [InlineKeyboardButton('remover produto(s)', callback_data= Menu.REMOVER_PRODUTO.value)],
            [InlineKeyboardButton('exibir pedido atual', callback_data=Menu.EXIBIR_ATUAL.value)],
            [InlineKeyboardButton('finalizar pedido', callback_data=Menu.FINALIZAR_PEDIDO.value)],
            [InlineKeyboardButton(msg_cancelar, callback_data=OPERACAO_CANCELAR)],
        ]
    else:
        botoes = [
            [InlineKeyboardButton('iniciar pedido', callback_data=Menu.INICIAR_PEDIDO.value)],
            [InlineKeyboardButton('exibir pedidos anteriores', callback_data=Menu.EXIBIR_ANTERIORES.value)],
            [InlineKeyboardButton(msg_cancelar, callback_data=OPERACAO_CANCELAR)],
        ]
    

    reply_markup = InlineKeyboardMarkup(botoes)
    
    await context.bot.send_message(chat_id=update.message.chat_id, text=msg, reply_markup=reply_markup)
    
async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    query = update.callback_query
    id_chamador = query.from_user.id


    #TODO correct with the next logic
    if id_chamador == context.user_data.get('authorized_user_id'):
        await query.edit_message_text(text=f'opcao selecionada {query.data}')
        
        if FLAG_PEDIDO == 0:
            if query.data == Menu.INICIAR_PEDIDO.value:
                FLAG_PEDIDO = 1
            elif query.data == OPERACAO_CANCELAR:
                msg = f'operacao cancelada'
                await query.edit_message_text(text=msg)
        else:
            if query.data == Menu.ADICIONAR_PRODUTO.value:
                pass
            elif query.data == Menu.REMOVER_PRODUTO.value:
                pass
            elif query.data == Menu.EXIBIR_ATUAL.value:
                pass
            elif query.data == Menu.FINALIZAR_PEDIDO.value:
                pass
            elif query.data == OPERACAO_CANCELAR:
                msg = f'operacao cancelada'
                await query.edit_message_text(text=msg)



    else:
        await query.answer(text=f'{query.from_user.first_name}, não foi você que chamou o menu!', show_alert=True)




def main():
    application = ApplicationBuilder().token(config.TOKEN).build()
    

    application.add_handler(CommandHandler('menu', menu_handler))
    application.add_handler(CallbackQueryHandler(menu_callback))


    # TODO decide the path of the conversation, implement the handlers
    # conv_handler = ConversationHandler(
    # entry_points=[CommandHandler("start", start)],
    # states={
    #     START_ROUTES: [
    #         CallbackQueryHandler(menu, pattern="^" + str(ONE) + "$"),
    #         CallbackQueryHandler(two, pattern="^" + str(TWO) + "$"),
    #         CallbackQueryHandler(three, pattern="^" + str(THREE) + "$"),
    #         CallbackQueryHandler(four, pattern="^" + str(FOUR) + "$"),
    #     ],
    #     END_ROUTES: [
    #         CallbackQueryHandler(start_over, pattern="^" + str(ONE) + "$"),
    #         CallbackQueryHandler(end, pattern="^" + str(TWO) + "$"),
    #     ],
    # },
    # fallbacks=[CommandHandler("start", start)],
    # )


    application.run_polling()


if __name__ == '__main__':
    main()

