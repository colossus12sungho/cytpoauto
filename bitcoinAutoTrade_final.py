import time
import pyupbit
import datetime
import requests
import json
import operator


access = "kdxhHTdscPwSzJkQ6gXm2aNxMcg3EJ0n4us75rVM"
secret = "H7uk9TQMQnVsoq3reKux3F7pz181IVi7E8DwAcca"
myToken = "xoxb-2883000978711-2899910699588-uFXvMZTFnDfxPnxdl4B1Wxkf"

def post_message(token, channel, text):
    """슬랙 메시지 전송"""
    response = requests.post("https://slack.com/api/chat.postMessage",
        headers={"Authorization": "Bearer "+token},
        data={"channel": channel,"text": text}
    )

def get_target_price(ticker, k):
    """변동성 돌파 전략으로 매수 목표가 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=2)
    target_price = df.iloc[0]['close'] + (df.iloc[0]['high'] - df.iloc[0]['low']) * k
    return target_price

def get_start_time(ticker):
    """시작 시간 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=1)
    start_time = df.index[0]
    return start_time

def get_ma15(ticker):
    """15일 이동 평균선 조회"""
    df = pyupbit.get_ohlcv(ticker, interval="day", count=15)
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






target_coin_origine = ['KRW-AAVE','KRW-1INCH','KRW-ADA','KRW-AERGO','KRW-AHT','KRW-ALGO','KRW-ANKR','KRW-AQT',
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

target_coin = ['KRW-POWR', 'KRW-BORA', 'KRW-BTC', 'KRW-CBK', 'KRW-ATOM', 'KRW-XRP', 'KRW-HUM', 'KRW-ELF', 'KRW-NEAR', 'KRW-SAND']

while True:
    try:
        now = datetime.datetime.now()
        start_time = get_start_time("KRW-SXP")
        end_time = start_time + datetime.timedelta(hours=24)

        if start_time < now < end_time - datetime.timedelta(minutes=30):

         #구매 
         i=0
         while i<10 :   
            target_price = get_target_price(target_coin[i], 0.35)
            ma15 = get_ma15(target_coin[i])
            current_price = get_current_price(target_coin[i])
            btc = get_balance(target_coin[i].replace("KRW-",""))
            if target_price < current_price and ma15 < current_price:
                krw = get_balance("KRW")
                if krw > 16000 and get_balance(target_coin[i].replace("KRW-",""))* get_current_price(target_coin[i]) < 200000 :
                    buy_result = upbit.buy_market_order(target_coin[i], krw*0.3)
                    time.sleep(0.5)
                    post_message(myToken,"#coin", target_coin[i] + " 매수 : " + str(buy_result["locked"]) + "원 (평단가 :" + str(upbit.get_avg_buy_price(target_coin[i])) + ")" )
        #손절
            if btc * get_current_price(target_coin[i]) > 5100  :
                avg_price = upbit.get_avg_buy_price(target_coin[i])
                profit_rate = ( (get_current_price(target_coin[i])-avg_price)/avg_price)
                if profit_rate < -0.04 : # 손절 비율
                    sell_result = upbit.sell_market_order(target_coin[i], btc)
                    post_message(myToken,"#coin", target_coin[i] + " 손절 : 평단가 : (" + str(avg_price) +"원) 매도가 : ("+ str(get_current_price(target_coin[i]))+"원)")
                    time.sleep(0.5)
            i=i+1

        else:
            #판매
         
         i=0
         while i <10 :
            btc = get_balance(target_coin[i].replace("KRW-",""))
            if btc * get_current_price(target_coin[i]) > 5100 :
                avg_price = upbit.get_avg_buy_price(target_coin[i])
                sell_result = upbit.sell_market_order(target_coin[i], btc)
                post_message(myToken,"#coin", target_coin[i] + " 정기매도 : 평단가 : (" + str(avg_price) +"원) 매도가 : ("+ str(get_current_price(target_coin[i]))+"원)")
            time.sleep(0.5)
            i=i+1  
          
         
         if end_time - datetime.timedelta(seconds=50) < now < end_time:
                My_previous_KRW=My_now_KRW
                My_now_KRW=pyupbit.get_balance_t(ticker='KRW', contain_req=False)
                post_message(myToken,"#coin", "사이클 종료 결과 : 잔고 KRW " + str(My_now_KRW) +"손익:" + str((My_now_KRW - My_previous_KRW) / My_previous_KRW )+"%")

                value =[]
                i= 0
                for i in target_coin_origine:
                 url = "https://api.upbit.com/v1/candles/minutes/240?market="+i+"&count=1"
                 headers = {"Accept": "application/json"}
                 response = requests.request("GET", url, headers=headers)

                 result = json.loads(response.text)
                 new_data1=result[0]

                 value.append(round(new_data1['candle_acc_trade_price'],-6)/1000000)
                 time.sleep(0.2)
                trade_price = dict(zip(target_coin_origine,value))
                Target_coin_sort = sorted(trade_price.items(), key=lambda item:item[1] ,reverse=True)
                new=list(dict(Target_coin_sort).keys())
                target_coin = new[0:10]  # 타겟 코인 반환
                post_message(myToken,"#coin", "변경 목표 코인 리스트 : " + str(target_coin) )
                time.sleep(50)
        
        time.sleep(1)
    except Exception as e:
        print(e,target_coin[i])
        post_message(myToken,"#coin", e)
        time.sleep(1)
