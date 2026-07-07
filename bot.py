import requests
from bs4 import BeautifulSoup
import os
from datetime import datetime

# GitHub Secrets မှ Token များ
BOT_TOKEN = os.getenv('BOT_TOKEN')
CHAT_ID = os.getenv('CHAT_ID')

def get_best_v2nodes():
    url = "https://v2nodes.com/country/sg/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers )
    soup = BeautifulSoup(response.text, 'html.parser')
    
    servers = []
    for h2 in soup.find_all('h2'):
        a_tag = h2.find('a', href=True)
        if a_tag and '/servers/' in a_tag['href']:
            link = "https://v2nodes.com" + a_tag['href']
            servers.append(link )
            if len(servers) >= 3: break
            
    final_configs = []
    for link in servers:
        try:
            res = requests.get(link, headers=headers)
            s = BeautifulSoup(res.text, 'html.parser')
            config = s.find('textarea', {'id': 'config'})
            if config:
                cfg_text = config.text.strip()
                proto_type = "TLS + WS"
                if "security=reality" in cfg_text: proto_type = "REALITY"
                elif "security=tls" in cfg_text: proto_type = "TLS"
                final_configs.append({"config": cfg_text, "type": proto_type})
        except: continue
    return final_configs

def format_and_send():
    configs = get_best_v2nodes()
    if not configs: return
    now = datetime.now().strftime("%d %b %Y")
    
    message = f"<b>MM Free VPN Hub</b>\n"
    message += f"🚀 <b>FREE VLESS KEYS | {now}</b> 🚀\n"
    message += f"📅 Daily Update\n"
    message += f"🌍 Singapore Servers\n"
    message += f"⚡ Fast • Stable • Free\n"
    message += f"━━━━━━━━━━━━━━━━━━━━\n\n"

    for i, item in enumerate(configs, 1):
        message += f"🔥 <b>VLESS #{i} | {item['type']}</b>\n"
        message += f"📍 SG Server\n\n"
        message += f"<code>copy</code>\n"
        message += f"<code>{item['config']}</code>\n"
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
    requests.post(url, json=payload )

if __name__ == "__main__":
    format_and_send()
