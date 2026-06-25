import telebot
from telebot import types
import requests

BOT_TOKEN = "8047429230:AAHFRqqe-We9a9hIrGMUwdEpdF7mAkeVre4"
API_URL = "https://ft-osint-api.duckdns.org/api/numleak?key=freetill1&num="
GROUP_URL = "https://t.me/oxaether_info"
bot = telebot.TeleBot(BOT_TOKEN, parse_mode="HTML")


def get_field(emoji, title, value):
    if not value or value == "N/A":
        return ""
    return f"┃ {emoji} <b>{title}:</b> <code>{value}</code>\n"


@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type in ['group', 'supergroup']:
        bot.reply_to(message, "🟢 <b>Bot is Active!</b>\n\n👉 <i>Use /num [number] to get info.</i>")
    else:
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("📢 ᴊᴏɪɴ ᴏᴜʀ ɢʀᴏᴜᴘ", url=GROUP_URL))
        bot.send_message(message.chat.id,
            "╭━━━〔 💎 <b>ᴏsɪɴᴛ ᴇɴɢɪɴᴇ</b> 〕━━━╮\n\n"
            "📱 <b>sᴇɴᴅ ᴀ 10 ᴅɪɢɪᴛ ɴᴜᴍʙᴇʀ</b>\n"
            "🔍 <b>ɪɴsᴛᴀɴᴛ ʟᴏᴏᴋᴜᴘ ʟᴇᴠᴇʟ 3</b>\n\n"
            "🔗 <b>ᴊᴏɪɴ ᴏᴜʀ ɢʀᴏᴜᴘ ᴛᴏ ᴜsᴇ ʙᴏᴛ!</b>\n"
            "╰━━━━━━━━━━━━━━━━━━━━━╯", reply_markup=markup)


@bot.message_handler(commands=['num'])
def num_lookup(message):
    args = message.text.split()
    if len(args) < 2:
        return bot.reply_to(message, "⚠️ <b>ᴜsᴀɢᴇ:</b> <code>/num 9876543210</code>")

    number = args[1]
    if not number.isdigit() or len(number) != 10:
        return bot.reply_to(message, "❌ <b>ɪɴᴠᴀʟɪᴅ 10 ᴅɪɢɪᴛ ɴᴜᴍʙᴇʀ!</b>")

    msg = bot.reply_to(message, "╭━━━〔 🔍 <b>ᴘʀᴏᴄᴇssɪɴɢ</b> 〕━━━╮\n\n📡 <i>ᴄᴏɴɴᴇᴄᴛɪɴɢ ᴛᴏ ᴅᴀᴛᴀʙᴀsᴇ...</i>")

    try:
        r = requests.get(API_URL + number, timeout=15)
        data = r.json() if r.status_code == 200 else None
    except:
        data = None

    if not data or not data.get("success"):
        return bot.edit_message_text("🚨 <b>ᴅᴀᴛᴀ ɴᴏᴛ ғᴏᴜɴᴅ ɪɴ ʟᴇᴀᴋ ᴅʙ!</b>", message.chat.id, msg.message_id)

    # ✅ FIX 1: use "or {}" so None from API doesn't crash .get()
    chain = data.get("chain") or {}
    records = chain.get("records", [])
    ct = data.get("calltracer") or {}

    res = f"╭━━━〔 🔍 <b>ᴏsɪɴᴛ ʀᴇᴘᴏʀᴛ: {number}</b> 〕━━━╮\n\n"

    if records:
        rec = records[0]
        phones = [rec.get(f"Phone{i}" if i > 1 else "Phone") for i in range(1, 7)
                  if rec.get(f"Phone{i}" if i > 1 else "Phone")]

        res += "╭━━━〔 💾 <b>ʟᴇᴀᴋᴇᴅ ᴅᴀᴛᴀ</b> 〕━━━╮\n"
        res += get_field("👤", "Name", rec.get("FullName"))
        res += get_field("👨", "Father", rec.get("FatherName"))
        res += get_field("📱", "Phones", " | ".join(phones))
        res += get_field("🆔", "Doc", rec.get("DocumentNumber"))
        res += get_field("🏠", "Address", rec.get("Adres", "").replace("!!", ", "))

    res += "\n╭━━━〔 📡 <b>ᴄᴀʟʟᴛʀᴀᴄᴇʀ ᴘʀᴏ</b> 〕━━━╮\n"
    res += get_field("📶", "SIM", ct.get("SIM card"))
    res += get_field("📍", "State", ct.get("Mobile State"))
    res += get_field("IP", "IP", ct.get("IP address"))
    res += get_field("🧠", "Person", ct.get("Owner Personality"))
    res += f"┃ ⏳ <b>Time:</b> <code>{data.get('response_time_ms')}ms</code>\n"
    res += "╰━━━━━━━━━━━━━━━━━━━━━╯\n\n"

    res += "╭━━━〔 🛡 <b>ᴅᴇᴠᴇʟᴏᴘᴇʀ ɪɴғᴏ</b> 〕━━━╮\n"
    res += "┃ 👨‍💻 <b>Dev:</b> <a href='https://t.me/AetheRxPy'>@AetheRxPy</a>\n"
    res += "┃ 📢 <b>Channel:</b> <a href='https://t.me/termuxcodex'>@termuxcodex</a>\n"
    res += "╰━━━━━━━━━━━━━━━━━━━━━╯"

    final_output = f"<blockquote>{res}</blockquote>"
    bot.edit_message_text(final_output, message.chat.id, msg.message_id)


print("Bot started...")
# ✅ FIX 2: higher timeout values to prevent ReadTimeout crashes
bot.infinity_polling(timeout=60, long_polling_timeout=60)
