import yfinance as yf
import pandas as pd
import requests

BOT_TOKEN = "8543130885:AAGf4e2BOclCnRdFR2bSCe0fUMhj0jPXufs"
CHAT_ID = "7084665160"

def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }
    requests.post(url, data=data)


VN30 = [
"ACB","BCM","BID","BVH","CTG","FPT","GAS","GVR","HDB","HPG",
"MBB","MSN","MWG","PLX","POW","SAB","SHB","SSB","SSI","STB",
"TCB","TPB","VCB","VHM","VIB","VIC","VJC","VNM","VPB","VRE"
]

signals = []

for stock in VN30:

    ticker = stock + ".VN"

    try:
        df = yf.download(ticker, period="6mo", interval="1d")

        if len(df) < 30:
            continue

        low_today = df["Low"].iloc[-1]
        low_20 = df["Low"].tail(20).min()

        vol_today = df["Volume"].iloc[-1]
        vol_avg = df["Volume"].tail(20).mean()

        close = df["Close"].iloc[-1]

        spring = low_today < low_20
        volume_spike = vol_today > vol_avg * 1.5

        if spring and volume_spike:

            msg = f"""
SPRING DETECTED

Stock: {stock}
Price: {round(close,2)}
Volume spike

Possible Wyckoff Spring
"""

            signals.append(msg)

    except:
        continue


if len(signals) == 0:

    send_telegram("VN30 Scan: No Spring today")

else:

    for s in signals:
        send_telegram(s)

print("SCAN COMPLETED")
