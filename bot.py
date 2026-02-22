import requests
import yfinance as yf
import pandas as pd

TOKEN = "8543130885:AAGf4e2BOclCnRdFR2bSCe0fUMhj0jPXufs"
CHAT_ID = "7084665160"

symbols = [
"ACB.VN","FPT.VN","VCB.VN","TCB.VN","MBB.VN",
"BID.VN","VNM.VN","HPG.VN","MSN.VN","VIC.VN"
]

def send(msg):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url,data={"chat_id":CHAT_ID,"text":msg})

def check(symbol):

    df = yf.download(symbol,interval="1d",period="3mo")

    if len(df)<20: return

    last = df.iloc[-1]
    test = df.iloc[-2]
    spring = df.iloc[-3]

    if spring['Low'] < df['Low'][-20:-3].min() and spring['Volume'] > df['Volume'][-20:-3].mean()*1.5:

        if test['Volume'] < spring['Volume']:

            if last['Close'] > last['Open'] and last['Volume'] > test['Volume']:

                buy = round(last['High'],2)
                sl  = round(spring['Low'],2)
                rr  = round((buy-sl)*2,2)

                msg = f"""
SPRING: {symbol}

Buy Stop: {buy}
Stoploss: {sl}
TP(2R): {buy+rr}
"""
                send(msg)

for s in symbols:
    check(s)
