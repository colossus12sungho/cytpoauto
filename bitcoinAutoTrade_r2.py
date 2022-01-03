import time
import pyupbit
import datetime
import requests
import json
import operator


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






target_coin_origine = ['KRW-SXP','KRW-BTC','KRW-SAND','KRW-ATOM','KRW-NEAR','KRW-POWR','KRW-XRP',
'KRW-ETH','KRW-KAVA','KRW-MATIC','KRW-STX','KRW-CVC','KRW-GAS','KRW-BORA','KRW-DAWN',
'KRW-DOGE','KRW-XTZ','KRW-SOL','KRW-BAT','KRW-ADA','KRW-REP','KRW-DOT','KRW-PLA','KRW-MANA',
'KRW-ALGO','KRW-LINK','KRW-VET','KRW-ICX','KRW-TRX','KRW-ONG', 'KRW-ELF' , 'KRW-ARDR', 'KRW-GAS']

target_coin = ['KRW-POWR', 'KRW-SXP', 'KRW-ELF', 'KRW-PLA', 'KRW-DAWN', 'KRW-BTC', 'KRW-SAND', 'KRW-BORA', 'KRW-STX', 'KRW-NEAR', 'KRW-XRP', 'KRW-CVC', 'KRW-MATIC', 'KRW-BAT']

while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-SXP")
        end_time = start_time + datetime.timedelta(minutes=240)

        if start_time < now < end_time - datetime.timedelta(seconds=60):

         #구매 
         i=0
         while i<14 :   
            target_price = get_target_price(target_coin[i], 0.35)
            ma15 = get_ma15(target_coin[i])
            current_price = get_current_price(target_coin[i])
            btc = get_balance(target_coin[i].replace("KRW-",""))
            if target_price < current_price and ma15 < current_price:
                krw = get_balance("KRW")
                if krw > 8400 and get_balance(target_coin[i].replace("KRW-",""))* get_current_price(target_coin[i]) < 100000 :
                    buy_result = upbit.buy_market_order(target_coin[i], krw*0.9995*0.6)
                    time.sleep(0.5)
                    post_message(myToken,"#coin", target_coin[i] + " 매수 : " + str(buy_result["locked"]) + "원 (평단가 :" + str(upbit.get_avg_buy_price(target_coin[i])) + ")" )
        #손절
            if btc * get_current_price(target_coin[i]) > 5500  :
                avg_price = upbit.get_avg_buy_price(target_coin[i])
                profit_rate = ( (get_current_price(target_coin[i])-avg_price)/avg_price)
                if profit_rate < -0.020 : # 손절 비율
                    sell_result = upbit.sell_market_order(target_coin[i], btc*0.9995)
                    post_message(myToken,"#coin", target_coin[i] + " 손절 : 평단가 : (" + str(avg_price) +"원) 매도가 : ("+ str(get_current_price(target_coin[i]))+"원)")
                    time.sleep(0.5)
            i=i+1

        else:
            #판매
         i=0
         while i <14 :
            btc = get_balance(target_coin[i].replace("KRW-",""))
            if btc * get_current_price(target_coin[i]) > 5500 :
                avg_price = upbit.get_avg_buy_price(target_coin[i])
                sell_result = upbit.sell_market_order(target_coin[i], btc*0.9995)
                post_message(myToken,"#coin", target_coin[i] + " 정기매도 : 평단가 : (" + str(avg_price) +"원) 매도가 : ("+ str(get_current_price(target_coin[i]))+"원)")
            time.sleep(0.5)
            i=i+1  

         if end_time - datetime.timedelta(seconds=30) < now < end_time:
                value =[]
                i= 0
                for i in target_coin_origine:
                 url = "https://api.upbit.com/v1/candles/minutes/240?market="+i+"&count=1"
                 headers = {"Accept": "application/json"}
                 response = requests.request("GET", url, headers=headers)

                 result = json.loads(response.text)
                 new_data1=result[0]

                 value.append(round(new_data1['candle_acc_trade_price'],-6)/1000000)
                 time.sleep(0.3)
                trade_price = dict(zip(target_coin_origine,value))
                Target_coin_sort = sorted(trade_price.items(), key=lambda item:item[1] ,reverse=True)
                new=list(dict(Target_coin_sort).keys())
                target_coin = new[0:14]  # 타겟 코인 반환
                post_message(myToken,"#coin", "변경 목표 코인 리스트 : " + str(target_coin) )
                time.sleep(30)
        
        time.sleep(1)
    except Exception as e:
        print(e,target_coin[i])
        post_message(myToken,"#coin", e)
        time.sleep(1)
