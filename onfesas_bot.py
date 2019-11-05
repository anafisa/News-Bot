import logging
from telegram.ext import Updater, CommandHandler, ConversationHandler, MessageHandler, Filters
from telegram import ReplyKeyboardMarkup, KeyboardButton
from parser import news, rss_news


updater = Updater(token='1041164852:AAFrXEoznar1FRMxuELTtgHrY-Ltv6N_SBs', use_context=True)
dispatcher = updater.dispatcher

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

ADD_CATEGORY, ADD_KEYWORD, ADD_RSS, RSS_KEYWORD = range(4)

dictionary = {'Science🎆': 'Наука и техника', 'Economy💰': 'Экономика', 'Internet📲': 'Интернет и СМИ',
              'Culture🕌': 'Культура', 'Travelling🏝': 'Путешествия', 'Life🏞': 'Из жизни',
              'Sport🏆': 'Спорт', 'World🌎': 'Мир', 'Russia🇷🇺': 'Россия'}


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id,
                             text="Hi Dear ✋ \nI'm News Bot 👨‍💻 \nI can show you all the latest news 📚\n"
                                  "What sphere are you interested in❓\nType <category> and choose one 📝\nOr <rss> to add your RSS 📲")


def choose_category(update, context):
    bot = context.bot
    keyboard = [
        [KeyboardButton("Science🎆")],
        [KeyboardButton("Economy💰")],
        [KeyboardButton("Internet📲")],
        [KeyboardButton("Culture🕌")],
        [KeyboardButton("Travelling🏝")],
        [KeyboardButton("Life🏞")],
        [KeyboardButton("Sport🏆")],
        [KeyboardButton("World🌎")],
        [KeyboardButton("Russia🇷🇺")]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard,
                                       one_time_keyboard=True,
                                       resize_keyboard=True)
    bot.send_message(update.message.chat_id, "Choose the category🔍",
                     reply_markup=reply_markup)
    return ADD_CATEGORY


def add_category(update, context):
    chat_data = context.chat_data
    chat_data['category'] = update.message.text
    context.bot.send_message(update.effective_chat.id,
                             text='Type the keyword✏️')
    return ADD_KEYWORD


def enter_rss(update, context):
    context.bot.send_message(update.effective_chat.id,
                             text='Enter RSS✏️')
    return ADD_RSS


def add_rss(update, context):
    chat_data = context.chat_data
    chat_data['rss'] = update.message.text
    context.bot.send_message(update.effective_chat.id,
                             text='Type the keyword✏️')
    return RSS_KEYWORD


def news_search_rss(update, context):
    chat_data = context.chat_data
    keyword = update.message.text
    rss = chat_data['rss']
    article = rss_news(rss, keyword)
    if article:
        for i in article:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"{i}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Sorry, I can't find appropriate news😔\nTry to enter another keyword🌸", )


def news_search(update, context):
    global dictionary
    chat_data = context.chat_data
    keyword = update.message.text
    category = dictionary[chat_data['category']]
    article = news(category, keyword)
    if article:
        for i in article:
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text=f"{i}")
    else:
        context.bot.send_message(chat_id=update.effective_chat.id,
                                 text="Sorry, I can't find appropriate news😔\nTry to enter another keyword🌸", )


def cancel(update, context):
    return ConversationHandler.END


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

choose_category_conversation = ConversationHandler(
    entry_points=[MessageHandler(Filters.regex("category"),
                                 choose_category),
                  MessageHandler(Filters.regex("rss"),
                                 enter_rss)],
    states={
        ADD_CATEGORY: [MessageHandler(Filters.text,
                                      add_category)],
        ADD_KEYWORD:  [MessageHandler(Filters.text,
                                     news_search),
                       MessageHandler(Filters.regex("category"),
                                     choose_category)],
        ADD_RSS:      [MessageHandler(Filters.text, add_rss)],

        RSS_KEYWORD:  [MessageHandler(Filters.text,
                                     news_search_rss),
                       MessageHandler(Filters.regex("rss"),
                                      enter_rss)]
    },
    fallbacks=[MessageHandler(Filters.all,cancel)])

dispatcher.add_handler(choose_category_conversation)

logging.info("start")
updater.start_polling(poll_interval=1)
