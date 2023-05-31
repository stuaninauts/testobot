import config
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, ContextTypes, CommandHandler


# habilita logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)



async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = f'msg de start'
    await context.bot.send_message(chat_id=update.message.chat_id, text=msg)


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    msg = f'msg de ajuda /comandos'
    #mensagem usando reply
    #await update.effective_message.reply_text(msg)
    await context.bot.send_message(chat_id=update.message.chat_id, text=msg)


async def teste(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.message.from_user
    chat_id = update.message.chat_id
    username = user.username
    first_name = user.first_name
    last_name = user.last_name

    print(f"ID do usuário: {chat_id}")
    print(f"Usernaxme: {username}")
    print('teste')
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


def main():
    application = ApplicationBuilder().token(config.TOKEN).build()
    
    application.add_handler(CommandHandler('start', start_handler))
    application.add_handler(CommandHandler('helpsm', help_handler))

    application.add_handler(CommandHandler('teste', teste))
    
    application.run_polling()


if __name__ == '__main__':
    main()

