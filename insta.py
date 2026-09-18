import os
import re
import asyncio

import instaloader

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

BOT_TOKEN = "8868187996:AAHugI62tsx2bvisTrQmpv5X8sOc9x_8OAI"
PASSWORD = "bl4cky"

authenticated_users = set()
usernames = {}


# ============================================================
# INSTALOADER
# ============================================================

L = instaloader.Instaloader(
    quiet=True,
    download_pictures=False,
    download_videos=False,
    download_video_thumbnails=False,
    download_geotags=False,
    download_comments=False,
    save_metadata=False,
)


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
        "│  ┌────────────────────┐  │\n"
        "│  │      • • • •       │  │\n"
        "│  └────────────────────┘  │\n"
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
# INSTAGRAM PROFILE CHECK
# ============================================================

def check_instagram_profile(username):

    username = username.replace("@", "").strip()

    # Basic username validation
    if not re.fullmatch(r"[A-Za-z0-9._]{1,30}", username):

        return {
            "success": False,
            "error": "Invalid Instagram username."
        }

    try:

        profile = instaloader.Profile.from_username(
            L.context,
            username
        )

        return {
            "success": True,

            "username": profile.username,

            "full_name": profile.full_name
            or "Not available",

            "followers": profile.followers,

            "following": profile.followees,

            "posts": profile.mediacount,

            "private": profile.is_private,

            "verified": profile.is_verified,

            "bio": profile.biography
            or "No bio",

            "profile_pic": profile.profile_pic_url,

            "external_url": profile.external_url,

            "url": f"https://www.instagram.com/{profile.username}/",

        }

    except instaloader.exceptions.ProfileNotExistsException:

        return {
            "success": False,
            "error": "Instagram profile does not exist."
        }

    except instaloader.exceptions.ConnectionException:

        return {
            "success": False,
            "error": (
                "Instagram connection failed.\n"
                "Try again after some time."
            )
        }

    except Exception as e:

        return {
            "success": False,
            "error": (
                "Unable to fetch profile information.\n\n"
                f"Reason: {str(e)}"
            )
        }


# ============================================================
# FORMAT PROFILE
# ============================================================

def format_profile(data):

    privacy = (
        "🔒 Private"
        if data["private"]
        else "🌐 Public"
    )

    verified = (
        "✅ Yes"
        if data["verified"]
        else "❌ No"
    )

    bio = data["bio"]

    # Prevent extremely long bio from making huge messages
    if len(bio) > 500:
        bio = bio[:500] + "..."

    external_url = data["external_url"]

    if not external_url:
        external_url = "None"

    text = (
        "╭──────────────────────────╮\n"
        "│   📸 INSTAGRAM PROFILE   │\n"
        "│         RESULTS          │\n"
        "╰──────────────────────────╯\n\n"

        f"👤 Username: @{data['username']}\n"
        f"📛 Name: {data['full_name']}\n\n"

        "📊 ACCOUNT STATS\n"
        "──────────────────────────\n"
        f"👥 Followers: {data['followers']:,}\n"
        f"➡️ Following: {data['following']:,}\n"
        f"📝 Posts: {data['posts']:,}\n\n"

        "🔐 ACCOUNT INFO\n"
        "──────────────────────────\n"
        f"🌐 Status: {privacy}\n"
        f"☑️ Verified: {verified}\n\n"

        "📝 BIO\n"
        "──────────────────────────\n"
        f"{bio}\n\n"

        "🔗 PROFILE\n"
        "──────────────────────────\n"
        f"{data['url']}\n\n"

        f"🌍 External link: {external_url}\n\n"

        "📅 Account creation date:\n"
        "❓ Not publicly available through "
        "Instagram profile data.\n\n"

        "⚠️ Only publicly available profile "
        "information is checked.\n\n"

        "By @tlg_Alam143"
    )

    return text


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
        context.user_data["waiting_username"] = True

        await query.message.reply_text(
            "📸 INSTAGRAM PROFILE CHECKER\n\n"
            "Send the Instagram username.\n\n"
            "Example:\n"
            "`instagram` \n\n"
            "or\n\n"
            "`@instagram`",
            parse_mode="Markdown"
        )

        return

    # --------------------------------------------------------
    # HELP
    # --------------------------------------------------------

    if data == "help":

        await query.message.reply_text(
            "ℹ️ HELP\n\n"
            "🔐 Login with password\n"
            "📸 Enter an Instagram username\n\n"
            "The checker can show publicly available "
            "profile information such as:\n\n"
            "👤 Username\n"
            "📛 Name\n"
            "👥 Followers\n"
            "➡️ Following\n"
            "📝 Posts\n"
            "🌐 Public / Private\n"
            "☑️ Verified status\n"
            "📝 Bio\n"
            "🔗 Profile URL\n\n"
            "⚠️ Instagram does not normally expose "
            "the exact account creation date on a "
            "public profile.",
            reply_markup=main_menu()
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

    if context.user_data.get("waiting_password"):

        context.user_data["waiting_password"] = False

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

    if context.user_data.get("waiting_username"):

        context.user_data["waiting_username"] = False

        username = text.replace("@", "").strip()

        if not username:

            await message.reply_text(
                "❌ Please enter a valid username."
            )

            return

        await message.reply_text(
            "🔎 Checking Instagram profile...\n"
            "Please wait..."
        )

        # Instaloader performs network I/O,
        # so run it outside the async event loop.
        data = await asyncio.to_thread(
            check_instagram_profile,
            username
        )

        if not data["success"]:

            await message.reply_text(
                "❌ PROFILE CHECK FAILED\n\n"
                f"{data['error']}\n\n"
                "Try another username later."
            )

            return

        usernames[user_id] = data["username"]

        result = format_profile(data)

        await message.reply_text(
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

    if BOT_TOKEN == "PUT_YOUR_NEW_BOT_TOKEN_HERE":

        print(
            "ERROR: Put your NEW Telegram BotFather "
            "token inside BOT_TOKEN."
        )

        return

    app = (
        Application.builder()
        .token(BOT_TOKEN)
        .build()
    )

    app.add_handler(
        CommandHandler("start", start)
    )

    app.add_handler(
        CallbackQueryHandler(button_handler)
    )

    app.add_handler(
        MessageHandler(
            filters.TEXT & ~filters.COMMAND,
            message_handler
        )
    )

    print("🤖 Instagram Profile Checker is running...")

    app.run_polling()


# ============================================================
# RUN
# ============================================================

if __name__ == "__main__":
    main()
