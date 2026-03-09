import yfinance as yf
import pandas as pd
import requests

# ===== TELEGRAM =====
BOT_TOKEN = "8543130885:AAGf4e2BOclCnRdFR2bSCe0fUMhj0jPXufs"
CHAT_ID = "7084665160"

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }
    requests.post(url, data=payload)

# ===== STOCK LIST =====
stocks = [
"ACB.VN","BCM.VN","BID.VN","BVH.VN","CTG.VN","FPT.VN","GAS.VN","GVR.VN",
"HDB.VN","HPG.VN","MBB.VN","MSN.VN","MWG.VN","PLX.VN","POW.VN","SAB.VN",
"SHB.VN","SSB.VN","SSI.VN","STB.VN","TCB.VN","TPB.VN","VCB.VN","VHM.VN",
"VIB.VN","VIC.VN","VJC.VN","VNM.VN","VPB.VN","VRE.VN",

"DXG.VN","DIG.VN","PDR.VN","NLG.VN","KDH.VN","NVL.VN",
"VND.VN","HCM.VN","VCI.VN","CTS.VN","BSI.VN",
"DPM.VN","DCM.VN","GMD.VN","REE.VN","PC1.VN",
"ANV.VN","IDI.VN","VHC.VN","ASM.VN",
"HHV.VN","CII.VN","HT1.VN","KBC.VN"
]

signals = []

for stock in stocks:

    try:

        df = yf.download(stock, period="6mo", interval="1d")

        if len(df) < 30:
            continue

        df["low20"] = df["Low"].rolling(20).min()
        df["vol_avg"] = df["Volume"].rolling(20).mean()

        today = df.iloc[-1]
        yesterday = df.iloc[-2]
        prev = df.iloc[-3]

        today_low = float(today["Low"])
        today_close = float(today["Close"])
        today_volume = float(today["Volume"])

        prev_low20 = float(yesterday["low20"])
        vol_avg = float(today["vol_avg"])

        # ===== SPRING =====
        spring = today_low < prev_low20 and today_close > prev_low20

        # ===== VOLUME SPIKE =====
        volume_spike = today_volume > vol_avg * 1.5

        # ===== TEST =====
        test = today_low > float(prev["Low"])

        if spring and volume_spike and test:
            signals.append(stock.replace(".VN",""))

    except:
        continue

# ===== TELEGRAM MESSAGE =====

if len(signals) > 0:

    message = "🚨 WYCKOFF SPRING + TEST\n\n"

    for s in signals:
        message += f"{s}\n"

else:

    message = "Market Scan: No Spring today"

send_telegram(message)

print("SCAN COMPLETED")
