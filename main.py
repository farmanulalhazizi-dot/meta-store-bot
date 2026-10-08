import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = os.environ.get("BOT_TOKEN")

votes = {}
poll_options = ["Option A", "Option B", "Option C"]

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("Products", callback_data="products")],
        [InlineKeyboardButton("Voting / Poll", callback_data="poll")],
        [InlineKeyboardButton("Contact", callback_data="contact")]
    ]
    await update.message.reply_text(
        "Hello! Welcome to Meta Store\n\nChoose an option:",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def send_poll(msg_obj):
    keyboard = []
    for opt in poll_options:
        count = list(votes.values()).count(opt)
        keyboard.append([InlineKeyboardButton(f"{opt} ({count} votes)", callback_data=f"vote_{opt}")])
    keyboard.append([InlineKeyboardButton("Show Results", callback_data="results")])
    text = "Election / Voting\n\nChoose your favorite:\n\n"
    for opt in poll_options:
        count = list(votes.values()).count(opt)
        text += f"- {opt}: {count} votes\n"
    if hasattr(msg_obj, 'edit_message_text'):
        await msg_obj.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await msg_obj.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    user_id = q.from_user.id
    if q.data.startswith("vote_"):
        choice = q.data.replace("vote_", "")
        votes[user_id] = choice
        await send_poll(q)
    elif q.data in ["poll", "back"]:
        if q.data == "poll":
            await send_poll(q)
        else:
            keyboard = [
                [InlineKeyboardButton("Products", callback_data="products")],
                [InlineKeyboardButton("Voting / Poll", callback_data="poll")],
                [InlineKeyboardButton("Contact", callback_data="contact")]
            ]
            await q.edit_message_text("Hello! Welcome to Meta Store\n\nChoose an option:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif q.data == "results":
        total = len(votes)
        text = "Final Results:\n\n"
        for opt in poll_options:
            count = list(votes.values()).count(opt)
            text += f"{opt}: {count} votes\n"
        text += f"\nTotal: {total}"
        keyboard = [[InlineKeyboardButton("Back to Poll", callback_data="poll")]]
        await q.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))
    elif q.data == "products":
        await q.edit_message_text("Our Products: Meta Verified, Stars, TikTok Coins", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="back")]]))
    elif q.data == "contact":
        await q.edit_message_text("Contact: @YourUsername", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Back", callback_data="back")]]))

def main():
    if not BOT_TOKEN:
        print("BOT_TOKEN missing!")
        return
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.run_polling()

if __name__ == "__main__":
    main()
