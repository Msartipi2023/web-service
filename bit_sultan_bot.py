
import telebot
from telebot import types

# --- Configuration ---
TOKEN = "7316027594:AAFo5X5ZwcXMvJ1abpI_ssrUAxHSNyEKzek"
ADMIN_ID = 681139
WALLET_ADDRESS = "0x41608C2Ba2788E67fEB161a58B41Ec66C8f52139"
CHANNEL_USERNAME = "@bit_sultan_bot"

bot = telebot.TeleBot(TOKEN)

# --- User Data Storage ---
users_data = {}

# --- Referral Links ---
referral_links = {
    "FaucetPay": "https://faucetpay.io/?r=6900627",
    "Bitbarg": "https://bitbarg.com/join/92703354",
    "PPng": "https://ppng.ir/r/bV6AY",
    "AdBTC": "https://r.adbtc.top/3727058",
    "TrustDice": "https://trustdice.win/faucet/?ref=u_msartipii",
}

# --- Function to create a referral link ---
def create_referral_link(user_id):
    return f"https://t.me/{bot.get_me().username}?start={user_id}"

# --- Welcome Handler ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    user_lang = message.from_user.language_code

    if user_id not in users_data:
        referral_link = create_referral_link(user_id)
        users_data[user_id] = {'referral_link': referral_link, 'referrals': [], 'balance': 0.0}

    if message.text and message.text.startswith("/start "):
        referrer_id = int(message.text.split()[1])
        if referrer_id in users_data and user_id != referrer_id:
            if user_id not in users_data[referrer_id]['referrals']:
                users_data[referrer_id]['referrals'].append(user_id)
                bot.send_message(referrer_id, f"🎉 {message.from_user.first_name} با لینک شما عضو شد!")

    referral_link = users_data[user_id]['referral_link']

    markup = types.InlineKeyboardMarkup(row_width=2)
    for name, url in referral_links.items():
        markup.add(types.InlineKeyboardButton(name, url=url))

    if user_lang == "fa":
        welcome_text = (
            f"سلام! به ربات بیت سلطان خوش اومدی!\n\n"
            f"لینک دعوت تو: {referral_link}\n"
            f"با دعوت دوستانت کسب درآمد کن!"
        )
    else:
        welcome_text = (
            f"Welcome to Bit Sultan Bot!\n\n"
            f"Your referral link: {referral_link}\n"
            f"Invite friends and earn!"
        )

    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# --- Withdraw Command ---
@bot.message_handler(commands=['withdraw'])
def handle_withdraw(message):
    user_id = message.from_user.id
    balance = users_data.get(user_id, {}).get('balance', 0)
    if balance > 0:
        amount_after_fee = round(balance * 0.8, 6)
        bot.send_message(
            message.chat.id,
            f"موجودی شما: {balance} تتر\nبعد از ۲۰٪ کارمزد: {amount_after_fee} تتر\nبه آدرس {WALLET_ADDRESS} ارسال خواهد شد."
        )
        users_data[user_id]['balance'] = 0
    else:
        bot.send_message(message.chat.id, "موجودی شما کافی نیست.")

# --- Show Admin's Referral Links ---
@bot.message_handler(commands=['mylinks'])
def show_admin_links(message):
    if message.from_user.id != ADMIN_ID:
        return

    markup = types.InlineKeyboardMarkup(row_width=2)
    for name, url in referral_links.items():
        markup.add(types.InlineKeyboardButton(name, url=url))

    bot.send_message(message.chat.id, "لینک‌های درآمدزای شما:", reply_markup=markup)

# --- Auto Promotion (Example Message to Channels/Groups) ---
def auto_promote():
    promo_text = "با ربات بیت سلطان درآمد دلاری داشته باش! \nورود: https://t.me/bit_sultan_bot"
    try:
        bot.send_message(CHANNEL_USERNAME, promo_text)
    except:
        pass

# --- Start Bot ---
if __name__ == '__main__':
    auto_promote()  # تبلیغ خودکار در کانال هنگام اجرا
    bot.infinity_polling()
