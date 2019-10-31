from telegram.ext import CommandHandler, MessageHandler, Filters
import logging
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, ConversationHandler


updater = Updater(token='1041164852:AAFrXEoznar1FRMxuELTtgHrY-Ltv6N_SBs', use_context=True)
dispatcher = updater.dispatcher


logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                     level=logging.INFO)

f = 1

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi Dear ✋ \nI'm News Bot 👨‍💻 \nI can show you all the latest news 📚\nWhat sphere are you interested in❓\nType <category> and choose one 📝")



def show_categories(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Science🎆\nEconomy💰\nSport🏆\nInternet📲\nCulture🕌\nTravelling🏝\nLife🏞\nWorld🌎\nRussia🇷🇺")


def chosen_category(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="ger")
    return f


PROCESS_DATA = 0


def cancel(update, context):
    return ConversationHandler.END


def get_data_from_user(text):
    def func(update, context):
        bot = context.bot
        bot.send_message(update.message.chat_id, f"{text}")
        return PROCESS_DATA

    return func


choose_category_conversation = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex("category"),
                                 get_data_from_user)],
    states={
        PROCESS_DATA: [MessageHandler(Filters.regex("key word"), get_data_from_user)],
    },
    fallbacks=[MessageHandler(Filters.all, cancel)]
)

#
# dispatcher.add_handler(ConversationHandler(entry_points=[MessageHandler(Filters.regex("category"), show_categories),get_data_from_user() ],
#                                            states={
#                                                PROCESS_DATA: [],
#                                                s: [CallbackQueryHandler(second)]},
#                                            ))



start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

dispatcher.add_handler(MessageHandler(Filters.regex("category"), show_categories))
#
# dispatcher.add_handler(MessageHandler(Filters.regex("Economy"), chosen_category))

dispatcher.add_handler(choose_category_conversation)



logging.info("start")
updater.start_polling(poll_interval=1)
