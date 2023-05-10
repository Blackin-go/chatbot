import os
from dotenv import load_dotenv
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import openai

# Carrega as chaves de API do arquivo .env
load_dotenv()
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Configura a conexão com a API do Telegram
updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher

# Configura a conexão com a API do OpenAI
openai.api_key = OPENAI_API_KEY

# Cria um handler para o comando /start
def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Olá! Posso lhe ajudar com alguma receita hoje ?")

# Cria um handler para as mensagens do usuário
def chat(update, context):
    # Verifica se a mensagem não é do próprio bot
    if update.message.from_user.id == context.bot.id:
        return

    # Obtém a mensagem do usuário
    user_input = update.message.text

    # Envia a mensagem do usuário como prompt para o ChatGPT da OpenAI
    prompt = f"Usuário: {user_input}\nBot:"

    # Gera a resposta do ChatGPT
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=900,
        temperature=0.3,
        n=1,
        stop=None
    )

    # Obtém a resposta do ChatGPT
    chat_response = response.choices[0].text.strip()

    # Envia a resposta do ChatGPT de volta para o usuário
    context.bot.send_message(chat_id=update.effective_chat.id, text=chat_response)

# Registra os handlers com o dispatcher
start_handler = CommandHandler('start', start)
chat_handler = MessageHandler(Filters.text & ~Filters.command, chat)
dispatcher.add_handler(start_handler)
dispatcher.add_handler(chat_handler)

# Inicia o bot do Telegram
updater.start_polling()
