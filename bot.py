import yfinance as yf
import requests
import pandas as pd

# ===== TELEGRAM =====

TOKEN = "8543130885:AAGf4e2BOclCnRdFR2bSCe0fUMhj0jPXufs"
CHAT_ID = "7084665160"

def send_telegram(msg):
url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
data = {
"chat_id": CHAT_ID,
"text": msg
}
requests.post(url, data=data)

# ===== VN30 SYMBOLS =====

symbols = [
"ACB.VN","BCM.VN","BID.VN","BVH.VN","CTG.VN","FPT.VN","GAS.VN","GVR.VN","HDB.VN","HPG.VN",
"MBB.VN","MSN.VN","MWG.VN","PLX.VN","POW.VN","SAB.VN","SHB.VN","SSB.VN","SSI.VN","STB.VN",
"TCB.VN","TPB.VN","VCB.VN","VHM.VN","VIB.VN","VIC.VN","VJC.VN","VNM.VN","VPB.VN","VRE.VN"
]

def check(symbol):
try:
df = yf.download(symbol, interval="1d", period="3mo")

```
    if len(df) < 30:
        return

    df = df.dropna()

    spring = df.iloc[-3]
    test = df.iloc[-2]
    last = df.iloc[-1]

    avg_vol = df['Volume'].iloc[-23:-3].mean()
    lowest_low = df['Low'].iloc[-23:-3].min()

    # ===== SPRING =====
    if spring['Low'] < lowest_low and spring['Volume'] > avg_vol * 1.5:

        # ===== TEST =====
        if test['Volume'] < spring['Volume']:

            # ===== BUY TRIGGER =====
            if last['Close'] > last['Open'] and last['Volume'] > test['Volume']:

                buy = round(last['High'], 2)
                sl = round(spring['Low'], 2)
                tp = round(buy + (buy - sl) * 2, 2)

                msg = f"""
```

SPRING DETECTED 📈
Mã: {symbol.replace('.VN','')}

Buy Stop: {buy}
Stoploss: {sl}
TP(2R): {tp}
"""
send_telegram(msg)

```
except Exception as e:
    print(symbol, e)
```

for s in symbols:
check(s)
