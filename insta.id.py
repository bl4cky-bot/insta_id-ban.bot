import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    filters,
)

# =========================
# CONFIG
# =========================

BOT_TOKEN = os.getenv("BOT_TOKEN")
PASSWORD = "bl4cky"

WELCOME_IMAGE = "welcome.jpg"


# =========================
# UI TEXT
# =========================

WELCOME_TEXT = """
╭──────────────────────────────╮
│                              │
│       🌸 𝙒𝙀𝙇𝘾𝙊𝙈𝙀 🌸          │
│                              │
│      ✨ 𝘽𝙇𝟰𝘾𝙆𝙔_𝘼𝙍𝙈𝙔 ✨        │
│                              │
│         🤖 𝙈𝙀𝙏𝙃𝙊𝘿 𝘽𝙊𝙏         │
│                              │
│      🔐 𝙋𝙡𝙯 𝙚𝙣𝙩𝙚𝙧 𝙥𝙖𝙨𝙨𝙬𝙤𝙧𝙙   │
│                              │
╰──────────────────────────────╯

          — 𝘿𝙀𝙑𝙀𝙇𝙊𝙋𝙀𝘿 𝘽𝙔 𝘼𝙇𝘼𝙈 —
"""


LOGIN_SUCCESS = """
╭───────────────────────────────╮
│      🌸 𝘽𝙇𝟰𝘾𝙆𝙔_𝘼𝙍𝙈𝙔 🌸       │
│                               │
│       ✅ 𝙇𝙤𝙜𝙞𝙣 𝙎𝙪𝙘𝙘𝙚𝙨𝙨𝙛𝙪𝙡      │
│                               │
│         🤖 𝙈𝙀𝙏𝙃𝙊𝘿 𝘽𝙊𝙏         │
╰───────────────────────────────╯
"""


METHOD_TEXT = """
╭─────────────── ✦ ───────────────╮
│                                 │
│      🌸 𝘽𝙇𝟰𝘾𝙆𝙔_𝘼𝙍𝙈𝙔 🌸          │
│                                 │
│         ⚙️ 𝙈𝙀𝙏𝙃𝙊𝘿 𝙃𝙐𝘽          │
│     ─────────────────────       │
│                                 │
│    𝙎𝙚𝙡𝙚𝙘𝙩 𝙄𝘿 𝘾𝙖𝙩𝙚𝙜𝙤𝙧𝙮       │
│                                 │
╰─────────────────────────────────╯
"""


HELP_TEXT = """
╭─────────────── ✦ ───────────────╮
│      🌸 𝘽𝙇𝟰𝘾𝙆𝙔_𝘼𝙍𝙈𝙔 🌸          │
│                                  │
│             ℹ️ 𝙃𝙀𝙇𝙋             │
│      ─────────────────────       │
│                                  │
│  🤖 𝙃𝙤𝙬 𝙩𝙤 𝙪𝙨𝙚                 │
│                                  │
│  ① 𝙈𝙀𝙏𝙃𝙊𝘿 𝙤𝙥𝙚𝙣 𝙠𝙖𝙧𝙤             │
│  ② 𝙄𝘿 𝙘𝙖𝙩𝙚𝙜𝙤𝙧𝙮 𝙨𝙚𝙡𝙚𝙘𝙩 𝙠𝙖𝙧𝙤   │
│  ③ 𝙎𝙘𝙧𝙚𝙚𝙣 𝙥𝙚 𝙙𝙞𝙮𝙚 𝙤𝙥𝙩𝙞𝙤𝙣𝙨     │
│     𝙛𝙤𝙡𝙡𝙤𝙬 𝙠𝙖𝙧𝙤                │
│                                  │
╰──────────────────────────────────╯
"""


# =========================
# KEYBOARDS
# =========================

def enter_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔑 𝙀𝙉𝙏𝙀𝙍",
                callback_data="enter"
            )
        ]
    ])


def main_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "⚙️ 𝙈𝙀𝙏𝙃𝙊𝘿",
                callback_data="method"
            )
        ],
        [
            InlineKeyboardButton(
                "ℹ️ 𝙃𝙀𝙇𝙋",
                callback_data="help"
            )
        ]
    ])


def method_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "👤 𝙉𝙊 𝙁𝘼𝘾𝙀 𝙄𝘿",
                callback_data="noface"
            ),
            InlineKeyboardButton(
                "🌐 𝙋𝙐𝘽𝙇𝙄𝘾 𝙄𝘿",
                callback_data="public"
            )
        ],
        [
            InlineKeyboardButton(
                "🔒 𝙋𝙍𝙄𝙑𝘼𝙏𝙀 𝙄𝘿",
                callback_data="private"
            ),
            InlineKeyboardButton(
                "📢 𝙈𝙀𝙉𝙏𝙄𝙊𝙉 𝙄𝘿",
                callback_data="mention"
            )
        ],
        [
            InlineKeyboardButton(
                "💳 𝙋𝘼𝙄𝘿 𝙎𝙀𝙍𝙑𝙄𝘾𝙀",
                callback_data="paid"
            )
        ],
        [
            InlineKeyboardButton(
                "👥 𝙋𝘼𝙄𝘿 𝙁𝙊𝙇𝙇𝙊𝙒𝙀𝙍𝙎",
                callback_data="followers"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 𝘽𝘼𝘾𝙆",
                callback_data="back_main"
            )
        ]
    ])


def back_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "🔙 𝘽𝘼𝘾𝙆",
                callback_data="method"
            )
        ]
    ])


# =========================
# START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data.clear()

    if os.path.exists(WELCOME_IMAGE):

        with open(WELCOME_IMAGE, "rb") as photo:
            await update.message.reply_photo(
                photo=photo,
                caption=WELCOME_TEXT,
                reply_markup=enter_keyboard()
            )

    else:

        await update.message.reply_text(
            WELCOME_TEXT,
            reply_markup=enter_keyboard()
        )


# =========================
# BUTTON HANDLER
# =========================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query
    await query.answer()

    data = query.data

    # ENTER
    if data == "enter":

        context.user_data["waiting_password"] = True

        await query.message.reply_text(
            "🔐 𝙋𝙖𝙨𝙨𝙬𝙤𝙧𝙙 𝙚𝙣𝙩𝙚𝙧 𝙠𝙖𝙧𝙤:"
        )

        return

    # METHOD
    if data == "method":

        if not context.user_data.get("logged_in"):
            await query.message.reply_text(
                "🔒 𝙋𝙡𝙚𝙖𝙨𝙚 𝙡𝙤𝙜𝙞𝙣 𝙛𝙞𝙧𝙨𝙩."
            )
            return

        await query.edit_message_text(
            METHOD_TEXT,
            reply_markup=method_keyboard()
        )

        return

    # HELP
    if data == "help":

        await query.edit_message_text(
            HELP_TEXT,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🔙 𝘽𝘼𝘾𝙆",
                        callback_data="back_main"
                    )
                ]
            ])
        )

        return

    # BACK MAIN
    if data == "back_main":

        await query.edit_message_text(
            LOGIN_SUCCESS,
            reply_markup=main_keyboard()
        )

        return

    # CATEGORY
    categories = {
        "noface": "👤 𝙉𝙊 𝙁𝘼𝘾𝙀 𝙄𝘿",
        "public": "🌐 𝙋𝙐𝘽𝙇𝙄𝘾 𝙄𝘿",
        "private": "🔒 𝙋𝙍𝙄𝙑𝘼𝙏𝙀 𝙄𝘿",
        "mention": "📢 𝙈𝙀𝙉𝙏𝙄𝙊𝙉 𝙄𝘿",
        "paid": "💳 𝙋𝘼𝙄𝘿 𝙎𝙀𝙍𝙑𝙄𝘾𝙀",
        "followers": "👥 𝙋𝘼𝙄𝘿 𝙁𝙊𝙇𝙇𝙊𝙒𝙀𝙍𝙎",
    }

    if data in categories:

        selected = categories[data]

        await query.edit_message_text(
            f"""
╭──────────────────────────────╮
│                              │
│      🌸 𝘽𝙇𝟰𝘾𝙆𝙔_𝘼𝙍𝙈𝙔 🌸       │
│                              │
│       ⚙️ 𝙎𝙀𝙇𝙀𝘾𝙏𝙀𝘿          │
│                              │
│       {selected}       │
│                              │
│  🛠️ 𝙈𝙚𝙩𝙝𝙤𝙙 𝙨𝙚𝙡𝙚𝙘𝙩𝙚𝙙.        │
│                              │
╰──────────────────────────────╯

⚠️ 𝙉𝙚𝙭𝙩 𝙖𝙘𝙩𝙞𝙤𝙣 𝙘𝙖𝙣 𝙗𝙚 𝙖𝙙𝙙𝙚𝙙 𝙝𝙚𝙧𝙚.
""",
            reply_markup=back_keyboard()
        )

        return


# =========================
# PASSWORD HANDLER
# =========================

async def password_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    if not context.user_data.get("waiting_password"):
        return

    password = update.message.text.strip()

    context.user_data["waiting_password"] = False

    if password == PASSWORD:

        context.user_data["logged_in"] = True

        await update.message.reply_text(
            LOGIN_SUCCESS,
            reply_markup=main_keyboard()
        )

    else:

        await update.message.reply_text(
            "❌ 𝙒𝙧𝙤𝙣𝙜 𝙋𝙖𝙨𝙨𝙬𝙤𝙧𝙙!\n\n"
            "🔐 𝙋𝙡𝙚𝙖𝙨𝙚 𝙩𝙧𝙮 𝙖𝙜𝙖𝙞𝙣."
        )


# =========================
# MAIN
# =========================

def main():

    if not BOT_TOKEN:
        raise RuntimeError(
            "BOT_TOKEN environment variable nahi mili."
        )

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            password_handler
        )
    )

    print("🤖 Bot Started...")

    app.run_polling()


if __name__ == "__main__":
    main()