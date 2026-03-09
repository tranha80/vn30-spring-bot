import yfinance as yf
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

# VN30
"ACB.VN","BCM.VN","BID.VN","BVH.VN","CTG.VN","FPT.VN","GAS.VN","GVR.VN",
"HDB.VN","HPG.VN","MBB.VN","MSN.VN","MWG.VN","PLX.VN","POW.VN","SAB.VN",
"SHB.VN","SSB.VN","SSI.VN","STB.VN","TCB.VN","TPB.VN","VCB.VN","VHM.VN",
"VIB.VN","VIC.VN","VJC.VN","VNM.VN","VPB.VN","VRE.VN",

# BĐS
"DXG.VN","DIG.VN","PDR.VN","NLG.VN","KDH.VN","NVL.VN","SCR.VN","HDC.VN",

# Chứng khoán
"VND.VN","HCM.VN","VCI.VN","CTS.VN","BSI.VN","FTS.VN","AGR.VN",

# Ngân hàng
"EIB.VN","LPB.VN","OCB.VN","BVB.VN",

# Công nghiệp
"REE.VN","PC1.VN","GMD.VN","HHV.VN","CII.VN",

# Thủy sản
"VHC.VN","ANV.VN","IDI.VN","ASM.VN",

# Khác
"DPM.VN","DCM.VN","HT1.VN","KBC.VN","SZC.VN","PAN.VN"
]

signals = []

for stock in stocks:

    try:

        df = yf.download(stock, period="6mo", interval="1d", progress=False)

        if df is None or len(df) < 25:
            continue

        df = df.reset_index()

        low_today = float(df["Low"].iloc[-1])
        close_today = float(df["Close"].iloc[-1])
        volume_today = float(df["Volume"].iloc[-1])

        low20 = float(df["Low"].iloc[-21:-1].min())
        vol_avg = float(df["Volume"].iloc[-21:-1].mean())

        # ===== SPRING =====
        spring = low_today < low20 and close_today > low20

        # ===== VOLUME SPIKE =====
        volume_spike = volume_today > vol_avg * 1.5

        if spring and volume_spike:
            signals.append(stock.replace(".VN",""))

    except:
        continue


# ===== TELEGRAM MESSAGE =====

if len(signals) > 0:

    message = "🚨 WYCKOFF SPRING ALERT\n\n"

    for s in signals:
        message += f"{s}\n"

else:

    message = "Market Scan: No Spring today"

send_telegram(message)

print("SCAN COMPLETED")
