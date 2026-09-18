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

# Welcome image ka path
WELCOME_IMAGE = "welcome.jpg"


# =========================
# TEXT
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

          [ 🔑 𝙀𝙉𝙏𝙀𝙍 ]

       — 𝘿𝙀𝙑𝙀𝙇𝙊𝙋𝙀𝘿 𝘽𝙔 𝘼𝙇𝘼𝙈 —
"""


LOGIN_TEXT = """
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
│                                  │
│       🌸 𝘽𝙇𝟰𝘾𝙆𝙔_𝘼𝙍𝙈𝙔 🌸          │
│                                  │
│          ⚙️ 𝙈𝙀𝙏𝙃𝙊𝘿 𝙃𝙐𝘽          │
│      ─────────────────────       │
│                                  │
│     𝙎𝙚𝙡𝙚𝙘𝙩 𝙄𝘿 𝘾𝙖𝙩𝙚𝙜𝙤𝙧𝙮        │
│                                  │
╰──────────────────────────────────╯

       — 𝘿𝙀𝙑𝙀𝙇𝙊𝙋𝙀𝘿 𝘽𝙔 𝘼𝙇𝘼𝙈 —
"""


HELP_TEXT = """
╭─────────────── ✦ ───────────────╮
│                                  │
│       🌸 𝘽𝙇𝟰𝘾𝙆𝙔_𝘼𝙍𝙈𝙔 🌸          │
│                                  │
│            ℹ️ 𝙃𝙀𝙇𝙋              │
│      ─────────────────────       │
│                                  │
│  🤖 𝙃𝙤𝙬 𝙩𝙤 𝙪𝙨𝙚                  │
│                                  │
│  ① 𝙈𝙀𝙏𝙃𝙊𝘿 𝙤𝙥𝙚𝙣 𝙠𝙖𝙧𝙤              │
│  ② 𝙄𝘿 𝙘𝙖𝙩𝙚𝙜𝙤𝙧𝙮 𝙨𝙚𝙡𝙚𝙘𝙩 𝙠𝙖𝙧𝙤    │
│  ③ 𝙎𝙘𝙧𝙚𝙚𝙣 𝙥𝙚 𝙙𝙞𝙮𝙚 𝙞𝙣𝙨𝙩𝙧𝙪𝙘𝙩𝙞𝙤𝙣𝙨 │
│     𝙛𝙤𝙡𝙡𝙤𝙬 𝙠𝙖𝙧𝙤                │
│                                  │
│  ⚠️ 𝙐𝙨𝙚 𝙤𝙣𝙡𝙮 𝙛𝙤𝙧 𝙖𝙥𝙥𝙧𝙤𝙥𝙧𝙞𝙖𝙩𝙚 𝙪𝙨𝙚 │
│                                  │
╰──────────────────────────────────╯

       — 𝘿𝙀𝙑𝙀𝙇𝙊𝙋𝙀𝘿 𝘽𝙔 𝘼𝙇𝘼𝙈 —
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


def method_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⚙️ 𝙈𝙀𝙏𝙃𝙊𝘿", callback_data="method")
        ],
        [
            InlineKeyboardButton("ℹ️ 𝙃𝙀𝙇𝙋", callback_data="help")
        ]
    ])


def category_keyboard():
    return InlineKeyboardMarkup([
        [
            InlineKeyboardButton(
                "👤 𝙉𝙊 𝙁𝘼𝘾𝙀 𝙄𝘿",
                callback_data="cat_no_face"
            ),
            InlineKeyboardButton(
                "🌐 𝙋𝙐𝘽𝙇𝙄𝘾 𝙄𝘿",
                callback_data="cat_public"
            )
        ],
        [
            InlineKeyboardButton(
                "🔒 𝙋𝙍𝙄𝙑𝘼𝙏𝙀 𝙄𝘿",
                callback_data="cat_private"
            ),
            InlineKeyboardButton(
                "📢 𝙈𝙀𝙉𝙏𝙄𝙊𝙉 𝙄𝘿",
                callback_data="cat_mention"
            )
        ],
        [
            InlineKeyboardButton(
                "💳 𝙋𝘼𝙄𝘿 𝙎𝙀𝙍𝙑𝙄𝘾𝙀",
                callback_data="cat_paid_service"
            )
        ],
        [
            InlineKeyboardButton(
                "👥 𝙋𝘼𝙄𝘿 𝙁𝙊𝙇𝙇𝙊𝙒𝙀𝙍𝙎",
                callback_data="cat_paid_followers"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 𝘽𝘼𝘾𝙆",
                callback_data="back_login"
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
# /START
# =========================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):

    context.user_data["logged_in"] = False
    context.user_data["waiting_password"] = False

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

    # ENTER
    if query.data == "enter":

        context.user_data["waiting_password"] = True

        await query.message.reply_text(
            "🔐 𝙋𝙖𝙨𝙨𝙬𝙤𝙧𝙙 𝙚𝙣𝙩𝙚𝙧 𝙠𝙖𝙧𝙤:"
        )

    # METHOD
    elif query.data == "method":

        if not context.user_data.get("logged_in"):
            await query.message.reply_text(
                "🔐 𝙋𝙚𝙝𝙡𝙚 𝙡𝙤𝙜𝙞𝙣 𝙠𝙖𝙧𝙤."
            )
            return

        await query.message.edit_text(
            LOGIN_TEXT + "\n" +
            "\n".join([
                "        [ ⚙️ 𝙈𝙀𝙏𝙃𝙊𝘿 ]",
                "",
                "        [ ℹ️ 𝙃𝙀𝙇𝙋 ]",
                "",
                "     — 𝘿𝙀𝙑𝙀𝙇𝙊𝙋𝙀𝘿 𝘽𝙔 𝘼𝙇𝘼𝙈 —"
            ]),
            reply_markup=method_keyboard()
        )

    # HELP
    elif query.data == "help":

        await query.message.edit_text(
            HELP_TEXT,
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "🔙 𝘽𝘼𝘾𝙆",
                        callback_data="method"
                    )
                ]
            ])
        )

    # CATEGORY MENU
    elif query.data.startswith("cat_"):

        names = {
            "cat_no_face": "👤 𝙉𝙊 𝙁𝘼𝘾𝙀 𝙄𝘿",
            "cat_public": "🌐 𝙋𝙐𝘽𝙇𝙄𝘾 𝙄𝘿",
            "cat_private": "🔒 𝙋𝙍𝙄𝙑𝘼𝙏𝙀 𝙄𝘿",
            "cat_mention": "📢 𝙈𝙀𝙉𝙏𝙄𝙊𝙉 𝙄𝘿",
            "cat_paid_service": "💳 𝙋𝘼𝙄𝘿 𝙎𝙀𝙍𝙑𝙄𝘾𝙀",
            "cat_paid_followers": "👥 𝙋𝘼𝙄𝘿 𝙁𝙊𝙇𝙇𝙊𝙒𝙀𝙍𝙎",
        }

        selected = names.get(query.data, "𝙈𝙀𝙏𝙃𝙊𝘿")

        text = f"""
╭─────────────── ✦ ───────────────╮
│                                  │
│       🌸 𝘽𝙇𝟰𝘾𝙆𝙔_𝘼𝙍𝙈𝙔 🌸          │
│                                  │
│        ✅ 𝙎𝙚𝙡𝙚𝙘𝙩𝙚𝙙             │
│                                  │
│        {selected}       │
│                                  │
│     ℹ️ 𝙈𝙚𝙩𝙝𝙤𝙙 𝙢𝙤𝙙𝙪𝙡𝙚 𝙞𝙨          │
│        𝙥𝙡𝙖𝙘𝙚𝙝𝙤𝙡𝙙𝙚𝙧 𝙤𝙣𝙡𝙮.       │
│                                  │
╰──────────────────────────────────╯

       — 𝘿𝙀𝙑𝙀𝙇𝙊𝙋𝙀𝘿 𝘽𝙔 𝘼𝙇𝘼𝙈 —
"""

        await query.message.edit_text(
            text,
            reply_markup=back_keyboard()
        )

    # BACK TO LOGIN/METHOD
    elif query.data == "back_login":

        await query.message.edit_text(
            LOGIN_TEXT + "\n" +
            "\n".join([
                "        [ ⚙️ 𝙈𝙀𝙏𝙃𝙊𝘿 ]",
                "",
                "        [ ℹ️ 𝙃𝙀𝙇𝙋 ]",
                "",
                "     — 𝘿𝙀𝙑𝙀𝙇𝙊𝙋𝙀𝘿 𝘽𝙔 𝘼𝙇𝘼𝙈 —"
            ]),
            reply_markup=method_keyboard()
        )


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

    if password == PASSWORD:

        context.user_data["logged_in"] = True
        context.user_data["waiting_password"] = False

        await update.message.reply_text(
            LOGIN_TEXT,
            reply_markup=method_keyboard()
        )

    else:

        await update.message.reply_text(
            "❌ 𝙒𝙧𝙤𝙣𝙜 𝙋𝙖𝙨𝙨𝙬𝙤𝙧𝙙\n\n"
            "🔐 𝘼𝙜𝙖𝙞𝙣 𝙩𝙧𝙮 𝙠𝙖𝙧𝙤:"
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

    app.add_handler(CommandHandler("start", start))

    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            password_handler
        )
    )

    print("🤖 Bot started...")
    app.run_polling()


if __name__ == "__main__":
    main()
