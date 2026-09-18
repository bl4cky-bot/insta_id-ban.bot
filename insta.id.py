import os
import re
import asyncio
import requests

from telegram import (
    Update,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
)

from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    CallbackQueryHandler,
    ContextTypes,
    filters,
)


# ============================================================
# CONFIG
# ============================================================

# IMPORTANT:
# Apna NEW BotFather token yahan paste karo.
BOT_TOKEN = os.getenv("8868187996:AAHugI62tsx2bvisTrQmpv5X8sOc9x_8OAI")

# Apna bot password yahan set karo.
PASSWORD = os.getenv("CHECKER_PASSWORD", "CHANGE_THIS_PASSWORD")

authenticated_users = set()
usernames = {}


# ============================================================
# INSTAGRAM REQUEST SETTINGS
# ============================================================

INSTAGRAM_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Linux; Android 10; K) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/140.0.0.0 Mobile Safari/537.36"
    ),
    "Accept": (
        "text/html,application/xhtml+xml,"
        "application/xml;q=0.9,*/*;q=0.8"
    ),
    "Accept-Language": "en-US,en;q=0.9",
}


# ============================================================
# UI
# ============================================================

def login_screen():

    text = (
        "╭──────────────────────────╮\n"
        "│   📸 INSTAGRAM PROFILE   │\n"
        "│         CHECKER          │\n"
        "├──────────────────────────┤\n"
        "│                          │\n"
        "│  🔐 SECURE ACCESS        │\n"
        "│                          │\n"
        "│  Enter Password          │\n"
        "│                          │\n"
        "│       [ 🔓 LOGIN ]       │\n"
        "│                          │\n"
        "╰──────────────────────────╯\n"
        "       By @tlg_Alam143"
    )

    keyboard = [
        [
            InlineKeyboardButton(
                "🔓 LOGIN",
                callback_data="login"
            )
        ]
    ]

    return text, InlineKeyboardMarkup(keyboard)


def main_menu():

    keyboard = [
        [
            InlineKeyboardButton(
                "📸 Instagram Profile",
                callback_data="instagram"
            )
        ],
        [
            InlineKeyboardButton(
                "ℹ️ Help",
                callback_data="help"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


def instagram_back_menu():

    keyboard = [
        [
            InlineKeyboardButton(
                "🔍 Check Another",
                callback_data="instagram"
            )
        ],
        [
            InlineKeyboardButton(
                "🔙 Main Menu",
                callback_data="back_main"
            )
        ],
    ]

    return InlineKeyboardMarkup(keyboard)


# ============================================================
# USERNAME CLEANER
# ============================================================

def clean_username(text):

    text = text.strip()

    # Instagram URL support
    text = re.sub(
        r"^https?://(www\.)?instagram\.com/",
        "",
        text,
        flags=re.IGNORECASE
    )

    # Remove query / trailing slash
    text = text.split("?")[0]
    text = text.strip("/")

    # Remove @
    text = text.lstrip("@")

    return text


# ============================================================
# INSTAGRAM PROFILE CHECK
# ============================================================

def check_instagram_profile(username):

    username = clean_username(username)

    # Instagram username validation
    if not re.fullmatch(
        r"[A-Za-z0-9._]{1,30}",
        username
    ):
        return {
            "success": False,
            "error": "Invalid Instagram username."
        }

    profile_url = (
        f"https://www.instagram.com/{username}/"
    )

    # Try twice
    for attempt in range(2):

        try:

            response = requests.get(
                profile_url,
                headers=INSTAGRAM_HEADERS,
                timeout=12,
                allow_redirects=True
            )

            # ------------------------------------------------
            # PROFILE DOES NOT EXIST
            # ------------------------------------------------

            if response.status_code == 404:

                return {
                    "success": False,
                    "error": (
                        "Instagram profile does not exist."
                    )
                }

            # ------------------------------------------------
            # RATE LIMIT
            # ------------------------------------------------

            if response.status_code == 429:

                if attempt == 0:
                    continue

                return {
                    "success": False,
                    "error": (
                        "Instagram is temporarily "
                        "rate-limiting requests.\n\n"
                        "Please try again later."
                    )
                }

            # ------------------------------------------------
            # OTHER HTTP ERROR
            # ------------------------------------------------

            if response.status_code != 200:

                if attempt == 0:
                    continue

                return {
                    "success": False,
                    "error": (
                        "Instagram returned HTTP "
                        f"{response.status_code}."
                    )
                }

            html = response.text

            # ------------------------------------------------
            # NOT AVAILABLE PAGE
            # ------------------------------------------------

            not_found_phrases = [
                "Sorry, this page isn't available.",
                "Page Not Found",
                "The link you followed may be broken",
            ]

            if any(
                phrase in html
                for phrase in not_found_phrases
            ):

                return {
                    "success": False,
                    "error": (
                        "Instagram profile does not exist."
                    )
                }

            # ------------------------------------------------
            # SUCCESS
            # ------------------------------------------------

            return {
                "success": True,

                "username": username,

                "full_name": (
                    "Public profile found"
                ),

                "followers": None,

                "following": None,

                "posts": None,

                "private": None,

                "verified": None,

                "bio": (
                    "Profile exists on Instagram."
                ),

                "profile_pic": None,

                "external_url": None,

                "url": profile_url,
            }

        except requests.Timeout:

            if attempt == 0:
                continue

            return {
                "success": False,
                "error": (
                    "Instagram request timed out.\n"
                    "Please try again."
                )
            }

        except requests.RequestException:

            if attempt == 0:
                continue

            return {
                "success": False,
                "error": (
                    "Instagram connection failed.\n"
                    "Please try again later."
                )
            }

        except Exception:

            return {
                "success": False,
                "error": (
                    "Unable to check this profile."
                )
            }

    return {
        "success": False,
        "error": "Unable to check Instagram profile."
    }


# ============================================================
# FORMAT PROFILE
# ============================================================

def format_profile(data):

    text = (
        "╭──────────────────────────╮\n"
        "│   📸 INSTAGRAM PROFILE   │\n"
        "│         RESULTS          │\n"
        "╰──────────────────────────╯\n\n"

        f"👤 Username: "
        f"@{data['username']}\n\n"

        "✅ PROFILE STATUS\n"
        "──────────────────────────\n"
        "🟢 Profile exists\n"
        "📡 Instagram profile found\n\n"

        "🔗 PROFILE\n"
        "──────────────────────────\n"
        f"{data['url']}\n\n"

        "ℹ️ INFORMATION\n"
        "──────────────────────────\n"
        "This checker verifies that the "
        "Instagram profile is publicly "
        "reachable.\n\n"

        "⚠️ Instagram may restrict automated "
        "requests. If the check fails, try "
        "again later.\n\n"

        "🔐 No Instagram password was used.\n\n"

        "By @tlg_Alam143"
    )

    return text


# ============================================================
# START
# ============================================================

async def start(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id

    context.user_data.clear()

    if user_id in authenticated_users:

        await update.message.reply_text(
            "╭──────────────────────────╮\n"
            "│       📸 MAIN MENU       │\n"
            "├──────────────────────────┤\n"
            "│  Welcome back! 👋        │\n"
            "╰──────────────────────────╯\n\n"
            "Select an option:",
            reply_markup=main_menu()
        )

        return

    text, keyboard = login_screen()

    await update.message.reply_text(
        text,
        reply_markup=keyboard
    )


# ============================================================
# BUTTON HANDLER
# ============================================================

async def button_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    query = update.callback_query

    await query.answer()

    user_id = query.from_user.id
    data = query.data

    # --------------------------------------------------------
    # LOGIN
    # --------------------------------------------------------

    if data == "login":

        context.user_data["waiting_password"] = True

        await query.message.reply_text(
            "🔐 SECURE LOGIN\n\n"
            "Please enter your password:"
        )

        return

    # --------------------------------------------------------
    # MAIN MENU
    # --------------------------------------------------------

    if data == "back_main":

        if user_id not in authenticated_users:

            await query.message.reply_text(
                "❌ Please login first."
            )

            return

        context.user_data.clear()

        await query.message.reply_text(
            "🏠 MAIN MENU\n\n"
            "Choose a feature:",
            reply_markup=main_menu()
        )

        return

    # --------------------------------------------------------
    # INSTAGRAM
    # --------------------------------------------------------

    if data == "instagram":

        if user_id not in authenticated_users:

            await query.message.reply_text(
                "❌ Login required."
            )

            return

        context.user_data.clear()

        context.user_data[
            "waiting_username"
        ] = True

        await query.message.reply_text(
            "📸 INSTAGRAM PROFILE CHECKER\n\n"
            "Send Instagram username.\n\n"
            "Examples:\n"
            "`instagram`\n"
            "`@instagram`\n"
            "`https://instagram.com/instagram/`",
            parse_mode="Markdown"
        )

        return

    # --------------------------------------------------------
    # HELP
    # --------------------------------------------------------

    if data == "help":

        await query.message.reply_text(
            "ℹ️ HELP\n\n"

            "🔐 Login with the bot password.\n\n"

            "📸 Then select Instagram Profile.\n\n"

            "🔎 Send a username like:\n"
            "`instagram`\n"
            "`@instagram`\n\n"

            "The checker verifies whether the "
            "profile is reachable.\n\n"

            "⚠️ Only publicly reachable information "
            "is checked.\n\n"

            "🔐 Never send your Instagram password "
            "to this bot.",
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )

        return


# ============================================================
# MESSAGE HANDLER
# ============================================================

async def message_handler(
    update: Update,
    context: ContextTypes.DEFAULT_TYPE
):

    user_id = update.effective_user.id
    message = update.message

    if not message or not message.text:
        return

    text = message.text.strip()

    # --------------------------------------------------------
    # PASSWORD
    # --------------------------------------------------------

    if context.user_data.get(
        "waiting_password"
    ):

        context.user_data[
            "waiting_password"
        ] = False

        if text == PASSWORD:

            authenticated_users.add(user_id)

            await message.reply_text(
                "✅ LOGIN SUCCESSFUL\n\n"
                "Welcome to Instagram Profile Checker.",
                reply_markup=main_menu()
            )

        else:

            await message.reply_text(
                "❌ WRONG PASSWORD\n\n"
                "Please try again."
            )

        return

    # --------------------------------------------------------
    # USERNAME
    # --------------------------------------------------------

    if context.user_data.get(
        "waiting_username"
    ):

        context.user_data[
            "waiting_username"
        ] = False

        username = clean_username(text)

        if not username:

            await message.reply_text(
                "❌ Please enter a valid "
                "Instagram username."
            )

            return

        checking_message = await message.reply_text(
            "🔎 Checking Instagram profile...\n"
            "Please wait..."
        )

        # Network request outside event loop
        data = await asyncio.to_thread(
            check_instagram_profile,
            username
        )

        # ----------------------------------------------------
        # FAILED
        # ----------------------------------------------------

        if not data["success"]:

            await checking_message.edit_text(
                "❌ PROFILE CHECK FAILED\n\n"
                f"{data['error']}\n\n"
                "Try another username or try again later."
            )

            return

        # ----------------------------------------------------
        # SUCCESS
        # ----------------------------------------------------

        usernames[user_id] = data["username"]

        result = format_profile(data)

        await checking_message.edit_text(
            result,
            reply_markup=instagram_back_menu()
        )

        return

    # --------------------------------------------------------
    # DEFAULT
    # --------------------------------------------------------

    if user_id not in authenticated_users:

        text_ui, keyboard = login_screen()

        await message.reply_text(
            text_ui,
            reply_markup=keyboard
        )

    else:

        await message.reply_text(
            "🏠 Please select an option:",
            reply_markup=main_menu()
        )


# ============================================================
# MAIN
# ============================================================

def main():

    if (
        not BOT_TOKEN
        or BOT_TOKEN == "PUT_YOUR_NEW_BOT_TOKEN_HERE"
    ):

        print(
            "ERROR: Add your NEW Telegram BotFather "
            "token to BOT_TOKEN."
        )

        return

    if (
        not PASSWORD
        or PASSWORD == "CHANGE_THIS_PASSWORD"
    ):

        print(
            "WARNING: Change CHECKER_PASSWORD "
            "before using the bot."
        )

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler(
            "start",
            start
        )
    )

    app.add_handler(
        CallbackQueryHandler(
            button_handler
        )
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message_handler
        )
    )

    print(
        "🤖 Instagram Profile Checker "
        "is running..."
    )

    app.run_polling()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()