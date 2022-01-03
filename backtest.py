import pyupbit
import numpy as np

df = pyupbit.get_ohlcv("KRW-XRP",interval="minute240", count=50)

# 변동폭 * k 계산 ( 고가-저가)*k 값
df['range'] = (df['high'] - df['low']) * 0.4
df['target'] = df['open'] + df['range'].shift(1)

fee = 0.0015

#ror(수익률)
df['ror'] = np.where(df['high'] > df['target'],
                     df['close'] / df['target'] - fee,
                     1)
# 누적 곱 계산(Cumprod) => 누적 수익률
df['hpr'] = df['ror'].cumprod()

# Draw Down 계산 ( 누적 최대 값과 현재 hpr 차이) / 누적 최대값 * 100)
df['dd'] = (df['hpr'].cummax() - df['hpr']) / df['hpr'].cummax() * 100
print("MDD(%): ", df['dd'].max())
df.to_excel("dd.xlsx")