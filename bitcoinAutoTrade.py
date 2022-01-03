import time
import pyupbit
import datetime
import requests

access = "kdxhHTdscPwSzJkQ6gXm2aNxMcg3EJ0n4us75rVM"
secret = "H7uk9TQMQnVsoq3reKux3F7pz181IVi7E8DwAcca"
myToken = "xoxb-2883000978711-2899910699588-bzLIuSFAI8pQ15XOLg6XmPPA"

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

# 로그인
upbit = pyupbit.Upbit(access, secret)
print("autotrade start")
# 시작 메세지 슬랙 전송
post_message(myToken,"#coin", "autotrade start")


target_coin = ["KRW-BTC","KRW-SAND","KRW-SXP","KRW-XRP","KRW-NEAR","KRW-ETH","KRW-MATIC","KRW-BORA","KRW-STX","KRW-ATOM","KRW-GLM","KRW-REP","KRW-BAT","KRW-CVC"]
target_sell_coin = ["BTC","SAND","SXP","XRP","NEAR","ETH","MATIC","BORA","STX","ATOM","GLM","REP","BAT","CVC"]


while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-SXP")
        end_time = start_time + datetime.timedelta(minutes=240)

        if start_time < now < end_time - datetime.timedelta(seconds=10):

         #구매 
         i=0
         while i<14 :   
            target_price = get_target_price(target_coin[i], 0.35)
            ma15 = get_ma15(target_coin[i])
            current_price = get_current_price(target_coin[i])
            if target_price < current_price and ma15 < current_price:
                krw = get_balance("KRW")
                if krw > 8400 and get_balance(target_sell_coin[i])* get_current_price(target_coin[i]) < 100000 :
                    buy_result = upbit.buy_market_order(target_coin[i], krw*0.9995*0.6)
                    post_message(myToken,"#coin", target_coin[i] +" Buy : " +str(buy_result))
            time.sleep(0.5)
            i=i+1

        else:
            #판매
         i=0
         while i <14 :
            btc = get_balance(target_sell_coin[i])
            if btc * get_current_price(target_coin[i]) > 5500 :
                sell_result = upbit.sell_market_order(target_coin[i], btc*0.9995)
                post_message(myToken,"#coin", target_coin[i] + " Sell : " +str(sell_result))
            time.sleep(0.5)
            i=i+1  

        time.sleep(1)
    except Exception as e:
        print(e,target_coin[i])
        post_message(myToken,"#coin", e)
        time.sleep(1)
