import time
import pyupbit
import datetime
import requests
import random
import json
import operator


access = "kdxhHTdscPwSzJkQ6gXm2aNxMcg3EJ0n4us75rVM"
secret = "H7uk9TQMQnVsoq3reKux3F7pz181IVi7E8DwAcca"
myToken = "xoxb-2883000978711-2899910699588-bzLIuSFAI8pQ15XOLg6XmPPA"

upbit = pyupbit.Upbit(access, secret)

def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute240", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute240", count=1)
    start_time = df.index[0]
    return start_time

def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="minute240", count=15)
    ma15 = df['close'].rolling(15).mean().iloc[-1]
    return ma15

def get_balance(ticker):
    """잔고 조회"""
    balances = upbit.get_balances()
    for b in balances:
        if b['currency'] == ticker:
            if b['balance'] is not None:
                return float(b['balance'])
            else:
                return 0
    return 0

def get_current_price(ticker):
    """현재가 조회"""
    return pyupbit.get_orderbook(ticker=ticker)["orderbook_units"][0]["ask_price"]

start = time.time()  # 시작 시간 저장


Target_coin = ['KRW-AAVE','KRW-1INCH','KRW-ADA','KRW-AERGO','KRW-AHT','KRW-ALGO','KRW-ANKR','KRW-AQT',
'KRW-ARDR','KRW-ARK','KRW-ATOM','KRW-AXS','KRW-BAT','KRW-BCH','KRW-BORA','KRW-BSV','KRW-BTC','KRW-BTG',
'KRW-BTT','KRW-CBK','KRW-CHZ','KRW-CRE','KRW-CRO','KRW-CVC','KRW-DAWN','KRW-DKA','KRW-DOGE','KRW-DOT',
'KRW-ELF','KRW-ENJ','KRW-EOS','KRW-ETC','KRW-ETH','KRW-FCT2','KRW-FLOW','KRW-GAS','KRW-GLM','KRW-GRS',
'KRW-HBAR','KRW-HIVE','KRW-HUM','KRW-HUNT','KRW-ICX','KRW-IOST','KRW-IOTA','KRW-IQ','KRW-JST','KRW-KAVA',
'KRW-KNC','KRW-LINK','KRW-LOOM','KRW-LSK','KRW-LTC','KRW-MANA','KRW-MATIC','KRW-MBL','KRW-MED','KRW-META',
'KRW-MFT','KRW-MLK','KRW-MOC','KRW-MTL','KRW-MVL','KRW-NEAR','KRW-NEO','KRW-NU','KRW-OMG','KRW-ONG','KRW-ONT',
'KRW-ORBS','KRW-PLA','KRW-POLY','KRW-POWR','KRW-PUNDIX','KRW-QKC','KRW-QTUM','KRW-REP','KRW-RFR','KRW-SAND','KRW-SBD',
'KRW-SC','KRW-SNT','KRW-SOL','KRW-SRM','KRW-SSX','KRW-STEEM','KRW-STMX','KRW-STORJ','KRW-STPT','KRW-STRAX','KRW-STRK',
'KRW-STX','KRW-SXP','KRW-TFUEL','KRW-THETA','KRW-TON','KRW-TRX','KRW-TT','KRW-UPP','KRW-VET','KRW-WAVES','KRW-WAXP','KRW-XEC',
'KRW-XEM','KRW-XLM','KRW-XRP','KRW-XTZ','KRW-ZIL','KRW-ZRX']



#print(Target_coin[0].replace("KRW-",""))

value =[]
i= 0
for i in Target_coin:

 url = "https://api.upbit.com/v1/candles/minutes/240?market="+i+"&count=1"
 headers = {"Accept": "application/json"}
 response = requests.request("GET", url, headers=headers)

 result = json.loads(response.text)
 
 new_data1=result[0]
 #new_data2=result[1]

 value.append(round(new_data1['candle_acc_trade_price'],-6)/1000000)

 time.sleep(0.1)

trade_price = dict(zip(Target_coin,value))

Target_coin_sort = sorted(trade_price.items(), key=lambda item:item[1] ,reverse=True)



new=list(dict(Target_coin_sort).keys())

final=[]
final = new[0:10]


print(Target_coin_sort)
print(str(final))
print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간