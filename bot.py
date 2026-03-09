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

# ===== VN30 LIST =====
vn30 = [
"ACB.VN","BCM.VN","BID.VN","BVH.VN","CTG.VN","FPT.VN","GAS.VN","GVR.VN",
"HDB.VN","HPG.VN","MBB.VN","MSN.VN","MWG.VN","PLX.VN","POW.VN","SAB.VN",
"SHB.VN","SSB.VN","SSI.VN","STB.VN","TCB.VN","TPB.VN","VCB.VN","VHM.VN",
"VIB.VN","VIC.VN","VJC.VN","VNM.VN","VPB.VN","VRE.VN"
]

spring_list = []

for stock in vn30:

    df = yf.download(stock, period="6mo", interval="1d")

    if len(df) < 20:
        continue

    low_20 = df["Low"].rolling(20).min()

    today_low = df["Low"].iloc[-1]
    prev_low = low_20.iloc[-2]

    close = df["Close"].iloc[-1]

    if today_low < prev_low and close > prev_low:
        spring_list.append(stock)

if len(spring_list) > 0:

    message = "VN30 SPRING DETECTED:\n"
    for s in spring_list:
        message += s + "\n"

else:

    message = "VN30 Scan: No Spring today"

send_telegram(message)

print("SCAN COMPLETED")
