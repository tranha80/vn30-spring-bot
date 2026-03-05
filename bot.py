import yfinance as yf
import requests
import pandas as pd

TOKEN = "8543130885:AAGf4e2BOclCnRdFR2bSCe0fUMhj0jPXufs"
CHAT_ID = "7084665160"

symbols = [
"ACB.VN","BCM.VN","BID.VN","BVH.VN","CTG.VN","FPT.VN","GAS.VN","GVR.VN","HDB.VN","HPG.VN",
"MBB.VN","MSN.VN","MWG.VN","PLX.VN","POW.VN","SAB.VN","SHB.VN","SSB.VN","SSI.VN","STB.VN",
"TCB.VN","TPB.VN","VCB.VN","VHM.VN","VIB.VN","VIC.VN","VJC.VN","VNM.VN","VPB.VN","VRE.VN"
]

def send_telegram(message):

    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "text": message
    }

    requests.post(url, data=payload)


def check_stock(symbol):

    df = yf.download(symbol, period="6mo", interval="1d")

    if len(df) < 30:
        return

    spring_low = df['Low'].iloc[-2]
    recent_low = df['Low'].iloc[-20:-3].min()

    spring_volume = df['Volume'].iloc[-2]
    avg_volume = df['Volume'].iloc[-20:-3].mean()

    if spring_low < recent_low and spring_volume > avg_volume * 1.5:

        price = df['Close'].iloc[-1]

        message = f"""
SPRING DETECTED

Stock: {symbol}
Price: {price}
"""

        send_telegram(message)


for s in symbols:
    try:
        check_stock(s)
    except:
        pass
