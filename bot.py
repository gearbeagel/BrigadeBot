import os
import telebot
from dotenv import load_dotenv

from models import VoiceMessage, session

load_dotenv('.env')
bot_token = os.getenv('BOT_TOKEN')

bot = telebot.TeleBot(bot_token)

bot.set_my_commands([telebot.types.BotCommand("start", "Запусти додіка"),
                     telebot.types.BotCommand("send", "Скинь додіку голосове"),
                     telebot.types.BotCommand("list", "Вивести список всіх голосових")])


@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Ку-у-у-у-у. Я бригадобот.\nМав би працювати за наступною командою: \n\n"
                                      "@brigadelorebot send <voice message name>\n\nЄбаш! 🎶")


@bot.message_handler(commands=['addvoice'])
def handle_addvoice_name(message):
    bot.send_message(message.chat.id, "Надішли голосове.")
    bot.register_next_step_handler(message, handle_voice_message)


@bot.message_handler(content_types=['voice'])
def handle_voice_message(message):
    if message.voice:
        name = message.caption
        if not name:
            bot.send_message(message.chat.id, "Дай назву голосового, далбайоб.")
            return
        save_voice_message(name, message.voice)


def save_voice_message(name, voice_message):
    voice_message = VoiceMessage(name=name, file_id=voice_message.file_id)
    session.add(voice_message)
    session.commit()


@bot.message_handler(commands=['send'])
def handle_send_command(message):
    command_parts = message.text.split(maxsplit=1)
    if len(command_parts) == 2:
        voice_message_name = command_parts[1]
        send_voice_message(message.chat.id, voice_message_name)
    else:
        bot.reply_to(message, "Напиши назву голосового.")


def send_voice_message(chat_id, voice_message_name):
    voice_message = session.query(VoiceMessage).filter(VoiceMessage.name.ilike(voice_message_name)).first()
    if voice_message:
        bot.send_voice(chat_id, voice_message.file_id, caption=voice_message.name)
    else:
        bot.send_message(chat_id, "Нема такого голосового, додік.")


@bot.message_handler(commands=['list'])
def handle_list_command(message):
    all_voice_messages = session.query(VoiceMessage).all()

    if all_voice_messages:
        voice_message_list = "\n".join([f"{i + 1}. {voice.name}" for i, voice in enumerate(all_voice_messages)])
        bot.send_message(message.chat.id, f"Доступні голосові:\n{voice_message_list}")
    else:
        bot.send_message(message.chat.id, "А нема ніхуя, блять.")


# Start the bot
bot.polling()
