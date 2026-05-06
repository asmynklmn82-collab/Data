import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import sqlite3
import requests
import json
import re

# إعدادات البوت
BOT_TOKEN = "8697100491:AAHFj14hZFIneFm2nWRNkpOrX6vshZsFu4o"

# إعداد التسجيل
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# أوامر البوت
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    welcome_text = """
**مرحبًا بك في بوت 💬 البحث المتقدم**

---

## ما الذي يمكنني فعله؟  
البحث عن أي رقم هاتف، بريد إلكتروني، أو حتى رقم قومي داخل قواعد بيانات ضخمة.

---

### بحث عن رقم أو بريد:  
- ارسل رقم الهاتف مباشرة مثل: 01011796996  
- أو أرسل البريد الإلكتروني للبحث عنه داخل التسريبات.

---

### تحليل الرقم القومي:  
- استخدم: /nid الرقم القومي  
- مثال: /nid 28007172400077

---

### أدوات فحص البريد:  
- /ghunt example@gmail.com – تحليل حساب Google (الصورة، المواقع، التعليقات)  
- /breachchecker example@email.com – فحص التسريبات عبر الإنترنت

---

### أدوات فيسبوك:  
- جلب صورة بروفايل الملف الشخصي المغلق - /fbp  
- بحث داخل منشورات - /fbsearch 01007185641

---

### Truecaller:  
- بحث متقدم عن أرقام الهواتف - /truecaller  
- بحث مباشر - /truecaller 01006963330
    """
    
    keyboard = [
        [InlineKeyboardButton("🔍 بحث برقم هاتف", callback_data="search_phone")],
        [InlineKeyboardButton("📧 بحث ببريد إلكتروني", callback_data="search_email")],
        [InlineKeyboardButton("🆔 تحليل رقم قومي", callback_data="nid_search")],
        [InlineKeyboardButton("📱 Truecaller", callback_data="truecaller")],
        [InlineKeyboardButton("🔐 فحص تسريبات", callback_data="breach_check")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(welcome_text, reply_markup=reply_markup, parse_mode='Markdown')

async def handle_phone_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    phone_number = update.message.text.strip()
    
    if not re.match(r'^01[0-9]{9}$', phone_number):
        await update.message.reply_text("❌ رقم الهاتف غير صحيح. يرجى إدخال رقم هاتف مصري صحيح (11 رقم)")
        return
    
    # محاكاة البحث في قواعد البيانات
    await update.message.reply_text(f"🔍 جاري البحث عن الرقم: {phone_number}")
    
    # محاكاة نتائج البحث
    results = f"""
**نتائج البحث عن الرقم: {phone_number}**

📞 **معلومات الرقم:**
- الناقل: {get_carrier(phone_number)}
- المنطقة: {get_region(phone_number)}

👤 **المعلومات الشخصية:**
- الاسم: محمد أحمد
- المحافظة: القاهرة

📱 **Truecaller:**
- الاسم: Mohamed Ahmed
- الصورة: متاحة

🔐 **التسريبات:**
- تم العثور على الرقم في 3 تسريبات
- آخر تسريب: 2023
    """
    
    await update.message.reply_text(results, parse_mode='Markdown')

async def nid_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ يرجى إدخال الرقم القومي بعد الأمر\nمثال: /nid 28007172400077")
        return
    
    nid = context.args[0]
    
    if not re.match(r'^[0-9]{14}$', nid):
        await update.message.reply_text("❌ الرقم القومي يجب أن يكون 14 رقم")
        return
    
    await update.message.reply_text(f"🔍 جاري تحليل الرقم القومي: {nid}")
    
    analysis = f"""
**تحليل الرقم القومي: {nid}**

📅 **التفاصيل:**
- تاريخ الميلاد: {nid[5:7]}/{nid[3:5]}/19{nid[1:3]}
- المحافظة: {get_governorate(nid[7:9])}
- النوع: {'ذكر' if int(nid[12]) % 2 == 1 else 'أنثى'}

📍 **المعلومات:**
- مركز الإصدار: القاهرة
- رقم السجل: {nid[9:13]}
    """
    
    await update.message.reply_text(analysis, parse_mode='Markdown')

async def ghunt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ يرجى إدخال البريد الإلكتروني بعد الأمر\nمثال: /ghunt example@gmail.com")
        return
    
    email = context.args[0]
    
    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        await update.message.reply_text("❌ بريد إلكتروني غير صحيح")
        return
    
    await update.message.reply_text(f"🔍 جاري تحليل حساب Google: {email}")
    
    analysis = f"""
**تحليل GHunt للبريد: {email}**

👤 **معلومات الحساب:**
- الاسم: محمد أحمد
- الصورة: ✓ متاحة
- الحساب: ✓ نشط

🌐 **الأنشطة:**
- YouTube: ✓ موجود
- Google Maps: ✓ موجود
- التعليقات: 15 تعليق

📊 **الإحصائيات:**
- تم إنشاء الحساب: 2020
- آخر نشاط: 2024
    """
    
    await update.message.reply_text(analysis, parse_mode='Markdown')

async def breach_checker(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ يرجى إدخال البريد الإلكتروني بعد الأمر\nمثال: /breachchecker example@email.com")
        return
    
    email = context.args[0]
    
    await update.message.reply_text(f"🔍 جاري فحص التسريبات للبريد: {email}")
    
    breach_info = f"""
**فحص التسريبات للبريد: {email}**

🔐 **نتائج الفحص:**
- العدد الإجمالي للتسريبات: 3
- كلمات المرور المسربة: 1
- آخر تسريب: 2023

📋 **التسريبات المكتشفة:**
1. LinkedIn (2021)
2. Facebook (2022) 
3. Adobe (2023)

⚠️ **التوصيات:**
- تغيير كلمة المرور
- تفعيل التحقق بخطوتين
    """
    
    await update.message.reply_text(breach_info, parse_mode='Markdown')

async def truecaller_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ يرجى إدخال رقم الهاتف بعد الأمر\nمثال: /truecaller 01006963330")
        return
    
    phone = context.args[0]
    
    await update.message.reply_text(f"🔍 جاري البحث في Truecaller عن: {phone}")
    
    truecaller_info = f"""
**نتائج Truecaller للرقم: {phone}**

👤 **المعلومات:**
- الاسم: محمد أحمد
- البريد: mohamed.ahmed@gmail.com
- المحافظة: القاهرة

📞 **تفاصيل الرقم:**
- الناقل: Vodafone
- النوع: جوال
- الحالة: ✓ نشط

📊 **التقييم:**
- التقييم: 4.2/5
- عدد التقيمات: 15
    """
    
    await update.message.reply_text(truecaller_info, parse_mode='Markdown')

async def facebook_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("❌ يرجى إدخال رقم الهاتف أو المعرف بعد الأمر\nمثال: /fbsearch 01007185641")
        return
    
    search_query = context.args[0]
    
    await update.message.reply_text(f"🔍 جاري البحث في فيسبوك عن: {search_query}")
    
    fb_info = f"""
**نتائج البحث في فيسبوك: {search_query}**

👤 **الملف الشخصي:**
- الاسم: Mohamed Ahmed
- الصورة: ✓ متاحة
- الأصدقاء: 350
- المنشورات: 45

📍 **المعلومات:**
- المحافظة: القاهرة
- العمل: مهندس برمجيات
- الدراسة: جامعة القاهرة

🔍 **المنشورات الأخيرة:**
- 3 منشورات هذا الشهر
- آخر نشاط: اليوم
    """
    
    await update.message.reply_text(fb_info, parse_mode='Markdown')

# دوال مساعدة
def get_carrier(phone):
    prefixes = {
        '010': 'Vodafone',
        '011': 'Etisalat', 
        '012': 'Orange',
        '015': 'WE'
    }
    return prefixes.get(phone[:3], 'غير معروف')

def get_region(phone):
    regions = ['القاهرة', 'الإسكندرية', 'الجيزة', 'الدقهلية', 'الشرقية']
    return regions[hash(phone) % len(regions)]

def get_governorate(code):
    gov_codes = {
        '01': 'القاهرة', '02': 'الإسكندرية', '03': 'بورسعيد',
        '04': 'السويس', '11': 'دمياط', '12': 'الدقهلية',
        '13': 'الشرقية', '14': 'القليوبية', '15': 'كفر الشيخ',
        '16': 'الغربية', '17': 'المنوفية', '18': 'البحيرة',
        '19': 'الإسماعيلية', '21': 'الجيزة', '22': 'بني سويف',
        '23': 'الفيوم', '24': 'المنيا', '25': 'أسيوط',
        '26': 'سوهاج', '27': 'قنا', '28': 'أسوان',
        '29': 'الأقصر', '31': 'البحر الأحمر', '32': 'الوادي الجديد',
        '33': 'مطروح', '34': 'شمال سيناء', '35': 'جنوب سيناء'
    }
    return gov_codes.get(code, 'غير معروف')

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == "search_phone":
        await query.edit_message_text("📞 أرسل رقم الهاتف للبحث (مثال: 01012345678)")
    elif query.data == "search_email":
        await query.edit_message_text("📧 أرسل البريد الإلكتروني للبحث")
    elif query.data == "nid_search":
        await query.edit_message_text("🆔 استخدم الأمر: /nid ثم الرقم القومي (14 رقم)")
    elif query.data == "truecaller":
        await query.edit_message_text("📱 استخدم الأمر: /truecaller ثم رقم الهاتف")
    elif query.data == "breach_check":
        await query.edit_message_text("🔐 استخدم الأمر: /breachchecker ثم البريد الإلكتروني")

def main():
    application = Application.builder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("nid", nid_command))
    application.add_handler(CommandHandler("ghunt", ghunt_command))
    application.add_handler(CommandHandler("breachchecker", breach_checker))
    application.add_handler(CommandHandler("truecaller", truecaller_search))
    application.add_handler(CommandHandler("fbsearch", facebook_search))
    application.add_handler(CommandHandler("fbp", facebook_search))
    
    application.add_handler(CallbackQueryHandler(button_handler))
    
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_phone_search))

    print("البوت يعمل الآن...")
    application.run_polling()

if __name__ == '__main__':
    main()
