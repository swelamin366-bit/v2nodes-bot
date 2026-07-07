import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime
import html

# GitHub Secrets မှ Token များ
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

def get_best_v2nodes():
    url = "https://v2nodes.com/country/sg/"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64 ) AppleWebKit/537.36'}
    print(f"Fetching V2Nodes from: {url}")
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        servers = []
        # Link များကို ပိုမိုတိကျစွာ ရှာဖွေခြင်း
        for a_tag in soup.find_all('a', href=True):
            if '/servers/' in a_tag['href']:
                link = "https://v2nodes.com" + a_tag['href']
                if link not in servers:
                    servers.append(link )
                if len(servers) >= 3: break
        
        print(f"Found {len(servers)} server links.")
        
        final_configs = []
        for link in servers:
            res = requests.get(link, headers=headers, timeout=15)
            s = BeautifulSoup(res.text, 'html.parser')
            config = s.find('textarea', {'id': 'config'})
            if config:
                cfg_text = config.text.strip()
                proto_type = "TLS + WS"
                if "reality" in cfg_text.lower(): proto_type = "REALITY"
                elif "tls" in cfg_text.lower(): proto_type = "TLS"
                final_configs.append({"config": cfg_text, "type": proto_type})
        
        return final_configs
    except Exception as e:
        print(f"Error fetching data: {e}")
        return []

def format_and_send():
    configs = get_best_v2nodes()
    if not configs:
        print("No configs found. Please check the website structure.")
        return

    now = datetime.now().strftime("%d %b %Y")
    
    message = f"<b>MM Free VPN Hub</b>\n"
    message += f"🚀 <b>FREE VLESS KEYS | {now}</b> 🚀\n"
    message += f"📅 Daily Update\n"
    message += f"🌍 Singapore Servers\n"
    message += f"⚡ Fast • Stable • Free\n"
    message += f"━━━━━━━━━━━━━━━━━━━━\n\n"

    for i, item in enumerate(configs, 1):
        # Config ထဲက < > & စတာတွေကို HTML format မပျက်အောင် escape လုပ်ခြင်း
        safe_config = html.escape(item['config'])
        message += f"🔥 <b>VLESS #{i} | {item['type']}</b>\n"
        message += f"📍 SG Server\n\n"
        message += f"<code>copy</code>\n"
        message += f"<code>{safe_config}</code>\n"
        message += f"━━━━━━━━━━━━━━━━━━━━\n\n"

    message += f"📥 <b>Import</b>\n"
    message += f"1️⃣ Copy Key\n"
    message += f"2️⃣ Open V2RayNG / V2Box\n"
    message += f"3️⃣ Import From Clipboard\n"
    message += f"4️⃣ Connect\n"
    message += f"⚠️ Free keys may expire anytime.\n"
    message += f"❤️ Share & Support The Channel\n\n"
    message += f"#VLESS #FreeVPN #Myanmar #V2Ray #VPNKeys"

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {"chat_id": CHAT_ID, "text": message, "parse_mode": "HTML", "disable_web_page_preview": True}
    
    response = requests.post(url, json=payload )
    print(f"Telegram API Response: {response.status_code}")
    print(f"Response Content: {response.text}")

if __name__ == "__main__":
    format_and_send()
