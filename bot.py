import yfinance as yf
import requests
import pandas as pd

TOKEN = "8543130885:AAGf4e2BOclCnRdFR2bSCe0fUMhj0jPXufs"
CHAT_ID = "7084665160"


def send_telegram(msg):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {
        "chat_id": CHAT_ID,
        "text": msg
    }
    requests.post(url, data=data)


VN30 = [
"ACB.VN","BCM.VN","BID.VN","BVH.VN","CTG.VN","FPT.VN","GAS.VN","GVR.VN",
"HDB.VN","HPG.VN","MBB.VN","MSN.VN","MWG.VN","PLX.VN","POW.VN","SAB.VN",
"SHB.VN","SSB.VN","SSI.VN","STB.VN","TCB.VN","TPB.VN","VCB.VN","VHM.VN",
"VIB.VN","VIC.VN","VJC.VN","VNM.VN","VPB.VN","VRE.VN"
]


def check_stock(symbol):

    df = yf.download(symbol, period="3mo", interval="1d")

    if df.empty:
        return

    spring = df.iloc[-1]
    prev = df.iloc[-20:-3]

    low_test = spring["Low"] < prev["Low"].min()
    vol_test = spring["Volume"] > prev["Volume"].mean() * 1.5
    bull_candle = spring["Close"] > spring["Open"]

    if low_test and vol_test and bull_candle:

        entry = round(spring["High"] * 1.01, 2)

        msg = f"""
SPRING DETECTED

Stock: {symbol}
Close: {spring['Close']}
Volume: {spring['Volume']}

Suggested BUY STOP: {entry}
"""
        send_telegram(msg)


for s in VN30:
    try:
        check_stock(s)
    except:
        pass
