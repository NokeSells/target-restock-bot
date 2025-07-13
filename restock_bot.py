import time
import requests
import random
from datetime import datetime, timedelta

WEBHOOK_URL = "https://discordapp.com/api/webhooks/1393705625472733288/fTR4pzeAnffnUMCkRuluB0jf-0TaLAZQdpM0UggMH3AW6IhtoUpeYo6o5kkMlswp1MTv"

TARGET_PRODUCTS = {
    "Product 1": "https://www.target.com/p/-/A-94636854",
    "Product 2": "https://www.target.com/p/-/A-94636851",
    "Product 3": "https://www.target.com/p/-/A-94636856",
    "Product 4": "https://www.target.com/p/-/A-94636862",
    "Product 5": "https://www.target.com/p/-/A-94681770",
    "Product 6": "https://www.target.com/p/-/A-94681785",
    "Product 7": "https://www.target.com/p/-/A-94636860"
}

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

# Track real in-stock products
in_stock_cache = {name: False for name in TARGET_PRODUCTS}

# Fake ping timing
next_fake_ping = datetime.now() + timedelta(minutes=random.randint(5, 12))

def send_discord_alert(name, url, fake=False):
    emoji = "🚨" if not fake else "👀"
    prefix = "" if not fake else "(Possible Restock?) "
    data = {
        "content": f"{emoji} {prefix}**{name}** is IN STOCK at Target!\n🔗 {url}"
    }
    try:
        requests.post(WEBHOOK_URL, json=data)
        tag = "Fake" if fake else "Real"
        print(f"✅ {tag} alert sent for: {name}")
    except Exception as e:
        print(f"❌ Failed to send alert for {name}: {e}")

def check_stock(name, url):
    global in_stock_cache
    try:
        response = requests.get(url, headers=HEADERS, timeout=10)
        content = response.text.lower()

        # Look for reliable "Add to Cart" button
        if 'data-test="addtocartbutton"' in content:
            if not in_stock_cache[name]:
                send_discord_alert(name, url)
                in_stock_cache[name] = True
            else:
                print(f"✅ Already in stock (no new ping): {name}")
        else:
            print(f"🔄 Still out of stock: {name}")
            in_stock_cache[name] = False
    except Exception as e:
        print(f"⚠️ Error checking {name}: {e}")

while True:
    now = datetime.now()

    # Real stock checks
    for name, url in TARGET_PRODUCTS.items():
        check_stock(name, url)

    # Check if it's time for a fake ping
    if now >= next_fake_ping:
        fake_name, fake_url = random.choice(list(TARGET_PRODUCTS.items()))
        send_discord_alert(fake_name, fake_url, fake=True)
        next_fake_ping = now + timedelta(minutes=random.randint(5, 12))

    time.sleep(5)
