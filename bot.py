import sys
if sys.version_info >= (3, 13):
    import imghdr
    sys.modules['imghdr'] = imghdr

import os
import json
import time
import logging
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
)

BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
ADMIN_ID = int(os.environ.get("ADMIN_ID", 0))
ADMIN_USERNAME = "@TreasureToolSupport"

UPI_ID = "k36672632@okicici"
QR_CODE_PATH = "qr.png"

COUPON_PRICES = {
    "myntra_100": {"label": "₹100 Myntra Coupon", "price": 35},
    "myntra_150": {"label": "₹150 Myntra Coupon", "price": 30},
}

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COUPONS_FILE = os.path.join(BASE_DIR, "coupons.json")
USERS_FILE = os.path.join(BASE_DIR, "users.json")
PENDING_ORDERS_FILE = os.path.join(BASE_DIR, "pending_orders.json")
FRAUD_FILE = os.path.join(BASE_DIR, "fraud_users.json")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def load_json(path, default):
    if not os.path.exists(path):
        return default
    with open(path, "r") as f:
        return json.load(f)

def save_json(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

def get_coupons():
    return load_json(COUPONS_FILE, {})

def get_users():
    return load_json(USERS_FILE, [])

def get_pending_orders():
    return load_json(PENDING_ORDERS_FILE, {})

def get_fraud_users():
    return load_json(FRAUD_FILE, [])

def add_user(user_id):
    users = get_users()
    if user_id not in users:
        users.append(user_id)
        save_json(USERS_FILE, users)

def stock_count(coupon_type):
    return len(get_coupons().get(coupon_type, []))

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    add_user(user.id)

    keyboard = [
        [InlineKeyboardButton("🟢 ₹100 Coupon — ₹35", callback_data="select_myntra_100")],
        [InlineKeyboardButton("🔵 ₹150 Coupon — ₹30", callback_data="select_myntra_150")],
    ]

    await update.message.reply_text(
        "🛍️ Welcome to Coupon Store\nSelect option:",
        reply_markup=InlineKeyboardMarkup(keyboard),
    )

async def handle_screenshot(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    await update.message.reply_text("Screenshot received")

    if update.message.photo:
        file_id = update.message.photo[-1].file_id
    else:
        return

    await context.bot.send_photo(
        chat_id=ADMIN_ID,
        photo=file_id,
        caption=f"User: {user.id}"
    )

async def main():
    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_screenshot))

    async with app:
        await app.start()
        await app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    asyncio.run(main())
