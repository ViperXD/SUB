from subtitle import BASE_URL, get_lang, search_sub
from messages import Messages
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext

def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        parse_mode="html",
        disable_web_page_preview=True,
        text=Messages.START.format(update.effective_user.id, update.effective_user.first_name),
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton('⚙ Channel ⚙', url='https://telegram.me/FayasNoushad'), InlineKeyboardButton('⚙ Group ⚙', url='https://telegram.me/FayasChat')]]),
    )

def searching(update: Update, context: CallbackContext):
    if update.message.via_bot != None:
        return

    search_message = context.bot.send_message(chat_id=update.effective_chat.id, text="Searching your subtitle file")
    sub_name = update.effective_message.text
    full_index, title, keyword = search_sub(sub_name)
    inline_keyboard = []
    if len(full_index) == 0:
        context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=search_message.message_id, text="No results found")
        return
    
    index = full_index[:15]
    for i in index:
        subtitle = title[i-1]
        key = keyword[i-1]
        inline_keyboard.append([InlineKeyboardButton(subtitle, callback_data=f"{key}")])

    reply_markup = InlineKeyboardMarkup(inline_keyboard)
    context.bot.edit_message_text(chat_id=update.effective_chat.id, message_id=search_message.message_id, text=f"Got the following results for your query *{sub_name}*. Select the preffered type from the below options", parse_mode="Markdown", reply_markup=reply_markup)
