import os
from telebot import TeleBot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv

# .env faylni yuklash
load_dotenv()

# Token va Admin ID-ni olish
TOKEN = os.getenv("TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Botni yaratish
bot = TeleBot(TOKEN)

# ===== Ma'lumotlar =====
info = {
    "🏫 Markaz haqida": """🏫 🟤 Muhsin ta’lim markazi 2021-yildan buyon faoliyat olib borib kelmoqda.  

💁‍♀️ Markazning asosiy g‘oyasi: yosh avlodni ummatga xizmat qilish ruhida tarbiyalash, kelajakda ummatni boshqara oladigan musulmonlarni yetkazib chiqarish.  

🔺 6 yoshdan 18 yoshgacha boʻlgan bolalar qabul qilinadi.  

🏠 Markazimizda quyidagi ilm fanlari o’qitiladi:  

🌙 **Diniy fanlar:**  
📚 Tajvid  
📚 Qurʼon  
📚 Arab tili  
📚 Duo  
📚 Odobnoma  
📚 Aqida  
📚 Hadis  
📚 Fiqh  
📚 Siyrat  

🎓 **Dunyoviy fanlar:**  
📚 Ona tili  
📚 Hisob/Matematika  
📚 O‘qish  
📚 Tabiatshunoslik  
📚 Mehnat  
📚 Sport  

🍲 Bolajonlarimizga 1 mahal issiq ovqat beriladi.
""",

    "👶 Bog‘cha haqida": """👶🌟 Farzandingiz kelajagi – biz bilan boshlanadi!  

📚 **Bizning bog‘cha haqida qisqacha:**  
👫 2 yoshdan 6 yoshgacha bo‘lgan bolalar qabul qilinadi.  
⏰ Ish vaqti: Har kuni 9:00 dan 15:15 gacha.  
🍲 Bolalar uchun 1 mahal issiq ovqat beriladi.  
🎓 Malakali o‘qituvchilar bolalarga bilim beradi.  
🎡 Bolalarga turli o‘yinlar va darslar o'tkaziladi.  

💫 Farzandingizni bog‘chaga yozdiring va uning ilk quvonchli qadamlariga guvoh bo‘ling!
"""
}

# ===== Videolar =====
videos = [
    {"title": "Madrasamiz", "url": "https://res.cloudinary.com/dngkszelu/video/upload/v1757247849/video_2025-09-07_13-19-18_fcovwl.mp4"},
    {"title": "Gazo yarmarka", "url": "https://res.cloudinary.com/dngkszelu/video/upload/v1757359007/video_2025-09-08_22-14-45_fnl3kx.mp4"},
    {"title": "Video 3", "url": "https://res.cloudinary.com/dngkszelu/video/upload/v1759091191/video_2025-09-28_23-25-48_djfbnq.mp4"},
    {"title": "Qizlar sinifi ", "url": "https://res.cloudinary.com/dngkszelu/video/upload/v1761495417/video_2025-10-26_19-15-37_fkgvqx.mp4"},
    {"title": "Ugil bolalar ", "url": "https://res.cloudinary.com/dngkszelu/video/upload/v1761496839/video_2025-10-26_19-40-06_djemky.mp4"}
]

# ===== Asosiy menyu =====
def main_menu():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🏫 Markaz haqida"),
        KeyboardButton("👶 Bog‘cha haqida"),
        KeyboardButton("📸 Instagram"),
        KeyboardButton("👩‍💼 Markaz ma'muriyati"),
        KeyboardButton("📚 Darslik videolar"),
        KeyboardButton("📍 Lokatsiya")
    )
    return markup

# ===== Inline tugmalar =====
def link_menu():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📸 Instagram", url="https://www.instagram.com/invites/contact/?utm_source=ig_contact_invite&utm_medium=copy_link&utm_content=z75sid7"))
    markup.add(InlineKeyboardButton("📍 Lokatsiya", url="https://maps.app.goo.gl/paG22uHdPJgBWLhS8"))
    return markup

def video_menu():
    markup = InlineKeyboardMarkup()
    for v in videos:
        markup.add(InlineKeyboardButton(v["title"], url=v["url"]))
    return markup

# ===== Xabarlarni qabul qilish =====
@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id, "Assalomu alaykum! 👋 Quyidagi menyudan foydalaning:", reply_markup=main_menu())

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    chat_id = message.chat.id
    text = message.text

    if text in info:  # Markaz yoki Bog‘cha haqida
        bot.send_message(chat_id, info[text], reply_markup=main_menu())

    elif text in ["📍 Lokatsiya", "📸 Instagram"]:
        bot.send_message(chat_id, "📌 Quyidagi havolalardan foydalaning:", reply_markup=link_menu())
        bot.send_message(chat_id, "👇 Asosiy menyu:", reply_markup=main_menu())

    elif text == "📚 Darslik videolar":
        bot.send_message(chat_id, "📚 Darslik videolar:", reply_markup=video_menu())
        bot.send_message(chat_id, "👇 Asosiy menyu:", reply_markup=main_menu())

    elif text == "👩‍💼 Markaz mamuriyati":
        bot.send_message(chat_id, "👩‍💼 Ma'muriyatga xabar yuboring. Siz yozgan xabar faqat adminga keladi.", reply_markup=main_menu())

    else:
        bot.send_message(chat_id, "👇 Quyidagi menyudan foydalaning:", reply_markup=main_menu())

        # Admin uchun foydalanuvchi xabarini yuborish
        if chat_id != ADMIN_ID:
            user_info = (
                f"👤 Yangi xabar:\n"
                f"🆔 ID: {chat_id}\n"
                f"📩 Matn: {text}\n"
                f"Telegram: @{message.from_user.username or '❌ username yo‘q'}"
            )
            bot.send_message(ADMIN_ID, user_info)

# ===== Botni ishga tushirish =====
print("🤖 Bot ishga tushdi...")
bot.polling(none_stop=True)
