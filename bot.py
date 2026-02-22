import yfinance as yf
import pandas as pd
import requests
import time

# ================= TELEGRAM =================

TOKEN = "8543130885:AAGf4e2BOclCnRdFR2bSCe0fUMhj0jPXufs"
CHAT_ID = "7084665160"

def send_telegram(msg):
url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
data = {"chat_id": CHAT_ID, "text": msg}
requests.post(url, data=data)

# ================= VN30 LIST =================

symbols = [
"ACB.VN","BCM.VN","BID.VN","BVH.VN","CTG.VN","FPT.VN","GAS.VN","GVR.VN","HDB.VN","HPG.VN",
"MBB.VN","MSN.VN","MWG.VN","PLX.VN","POW.VN","SAB.VN","SHB.VN","SSB.VN","SSI.VN","STB.VN",
"TCB.VN","TPB.VN","VCB.VN","VHM.VN","VIB.VN","VIC.VN","VJC.VN","VNM.VN","VPB.VN","VRE.VN"
]

# ================= MAIN LOGIC =================

def check(symbol):

```
df = yf.download(symbol, period="6mo", interval="1d", progress=False)

if len(df) < 30:
    return

# ----- SPRING NẾN -----
spring = df.iloc[-3]

# ----- TEST NẾN -----
test = df.iloc[-2]

# ----- BUY TRIGGER -----
trigger = df.iloc[-1]

# ----- VÙNG 20 NẾN TRƯỚC -----
zone_low = df.iloc[-22:-3]['Low'].min()
avg_vol  = df.iloc[-22:-3]['Volume'].mean()

# ================= SPRING =================
spring_condition = (
    spring['Low'] < zone_low and
    spring['Close'] > spring['Open'] and
    spring['Volume'] > avg_vol
)

# ================= TEST =================
test_condition = (
    test['Low'] >= spring['Low'] and
    test['Volume'] < spring['Volume']
)

# ================= BUY TRIGGER =================
trigger_condition = (
    trigger['Close'] > test['High'] and
    trigger['Volume'] > test['Volume']
)

if spring_condition and test_condition and trigger_condition:

    buy_stop = round(trigger['High'] * 1.01, 2)

    message = f"""
```

📈 WYCKOFF SPRING - VN30

Mã: {symbol.replace('.VN','')}
Buy Stop đề xuất: {buy_stop}

Spring ✔️
Test ✔️
Buy Trigger ✔️
"""
send_telegram(message)

# ================= RUN =================

for s in symbols:
try:
check(s)
time.sleep(3)
except:
pass
