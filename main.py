import time
import re
from datetime import date, datetime
import os
import math
from poloniex import Poloniex
# SQL connection
import mysql.connector
from mysql.connector import Error
from binance.client import Client
from binance.enums import *
#check
client = Client("", "", {"verify": True, "timeout": 20})



# while(True):
#     prices = client.get_symbol_ticker(symbol="ADAUSDT")
#     print(prices)
#     TotalPrice = float((prices.get('price')))
#     print(TotalPrice)
#     time.sleep(0.1)
#     orders = client.get_all_orders(symbol='ADAUSDT', limit=10)
#     print("prices",prices)
#     balance = client.get_asset_balance(asset='USDT')
#     print("balance",balance)
#     order = client.create_test_order(
#         symbol='ADAUSDT',
#         side=SIDE_BUY,
#         type=ORDER_TYPE_LIMIT,
#         timeInForce=TIME_IN_FORCE_GTC,
#         quantity=100, price='0.00001')
#
#     print("success")
#     time.sleep(100)


# SQL Connection
try:
    connection = mysql.connector.connect(host='192.168.1.32',
                                         port='3306',
                                         database='Operations',
                                         user='root',
                                         password='06021999')
    if connection.is_connected():
        db_Info = connection.get_server_info()
        print("Connected to MySQL Server version ", db_Info)
except Error as e:
    print("Error while connecting to MySQL", e)




# Global Variables
BalanceUSD = 1000.0
BalanceBTC = 0.00
# BalanceTotalUSD = 1000.0
total = []



# attemptToMakeTradeUsingThresholds
def attemptToMakeTrade(nextOperation,BTCvalue,balanceUSD,balanceBTC,total1):
    BalanceBTCT = 0
    BalanceUSDT = 0
    DipThreshold = 11735
    ProfitThreshold = 11790
    StopLossThreshold = 11200
    total1 = []
    if nextOperation == True and BTCvalue < DipThreshold:
        BalanceNew = tryToBuy(BTCvalue,balanceUSD,balanceBTC)
        BalanceUSDT = BalanceNew[0]
        BalanceBTCT = BalanceNew[1]
        total1 = [BalanceUSDT, BalanceBTCT, BalanceUSD + BTCvalue * BalanceBTC]
        return total1

    if nextOperation == False and (BTCvalue > ProfitThreshold or BTCvalue < StopLossThreshold):
        BalanceNew = tryToSell(BTCvalue,balanceUSD,balanceBTC)
        BalanceUSDT = BalanceNew[0]
        BalanceBTCT = BalanceNew[1]
        total1 = [BalanceUSDT, BalanceBTCT, BalanceUSD + BTCvalue * BalanceBTC]
        return total1
    else:
        total1 = [balanceUSD,balanceBTC,balanceUSD + BalanceBTC * BTCvalue]
        return total1



# Buy Operation Function_forThresholdsUsing
def tryToBuy(BTC,BLUSD,BLBTC):
    B = []
    BTCF = float(BTC)
    B.append(BLUSD /2)
    x = BLBTC + 0.5 * BLUSD / BTC
    B.append(x)
    connection = mysql.connector.connect(host='localhost',
                                         database='Operations',
                                         user='root',
                                         password='Ben206399073')
    cursor = connection.cursor()
    cursor.execute("INSERT INTO operations(BuyOrSell, BTCValue ) VALUES (%s,%s)", ("Buy", BTCF))
    connection.commit()
    connection.close()
    print('trytobuy')
    return B
# TryToBuy
def tryToBuy(BTC,BLUSD,BLBTC):
    print('TryToBuy')
    result_new = []
    AverageBTC = 0.00
    i = 0
    B = []
    # if BLBTC != 0 :
    #     B.append(BLBTC * BTC)
    # else :
    #     B.append(0)
    # B.append(BLUSD * 0)

    BTCF = float(BTC)
    connection = mysql.connector.connect(host='192.168.1.32',
                                         port='3306',
                                         database='Operations',
                                         user='root',
                                         password='06021999')
    cursor = connection.cursor()
    cursor.execute("select BTCValue from operations where BuyOrSell = 'Buy'")
    result = cursor.fetchall()
    for line in result :
        t= float(re.search(r'\d+', str(line)).group())
        result_new.append(t)

    for val in result_new:
        AverageBTC = AverageBTC + val
        i = i + 1

    AverageBTC = AverageBTC / i
    Buy_ROI = (BTC - AverageBTC) / AverageBTC

    # Change ROI range for buy operation is needed
    if Buy_ROI < -1:
    #      sellFunIsNeeded
    #      Then to get from thi fun the balances
    # to Insert the balances into B
        BLUSD_B4 = BLUSD
        BLUSD = BLUSD * ((100 + Buy_ROI * 1.5) / 100)
        BLBTC = BLBTC + (BLUSD_B4 - BLUSD) / BTC
        cursor.execute("INSERT INTO operations(BuyOrSell, BTCValue) VALUES (%s,%s)", ("Buy", BTCF))
        connection.commit()
        print('BUY succeded')
    else:
        print('BUY unsecceded')
    connection.close()
    B.append(BLUSD)
    B.append(BLBTC)


    # print('AllValues=' , result)
    # print (result_new)
    print('Buy ROI=',Buy_ROI)
    return B


# Sell Operation Function
def tryToSell(BTC,BLUSD,BLBTC):
    print('trytosell')
    result_new = []
    AverageBTC = 0.0001
    i = 1
    B = []
    # if BLBTC != 0 :
    #     B.append(BLBTC * BTC)
    # else :
    #     B.append(0)
    # B.append(BLUSD * 0)

    BTCF = float(BTC)
    connection = mysql.connector.connect(host='192.168.1.32',
                                         port='3306',
                                         database='Operations',
                                         user='root',
                                         password='06021999')
    cursor = connection.cursor()
    cursor.execute("select BTCValue from operations where BuyOrSell = 'Sell'")
    result = cursor.fetchall()
    for line in result :
        t= float(re.search(r'\d+', str(line)).group())
        result_new.append(t)


    for val in result_new:
        AverageBTC = AverageBTC + val
        i = i + 1

    AverageBTC = AverageBTC / i
    print(AverageBTC)
    Sell_ROI = (BTC - AverageBTC) / AverageBTC

    # Change ROI range for buy operation is needed
    if Sell_ROI > 1:
    #      sellFunctionIsNeeded
    #      Then to get from thi fun the balances
    # to Insert the balances into B
        BLUSD_B4 = BLUSD
        BLUSD = BLUSD * ((100 + Sell_ROI*1.5) / 100)
        BLBTC = BLBTC + (BLUSD-BLUSD_B4)/BTC
        # cursor.execute("INSERT INTO operations(BuyOrSell, BTCValue) VALUES (%s,%s)", ("Sell", BTCF))
        # connection.commit()
        print('Sold succeded')
    else:
        print('Sold unsecceded')
    connection.close()
    B.append(BLUSD)
    B.append(BLBTC)

    # print('AllValues=' , result)
    # print (result_new)
    print('Sell ROI=',Sell_ROI)
    return B



# Main !!
if __name__ == '__main__':
    TestingData=[]

    # Get Balances function is needed
    BalanceBTCT = 0
    BalanceUSDT = 0
    # Get Balances function is needed
    IsNextOperationBuy = True
    totalMain = []
    LastOpPrice = 100

    # GetTestingData
    # connection = mysql.connector.connect(host='192.168.1.32',
    #                                      port='3306',
    #                                      database='Operations',
    #                                      user='root',
    #                                      password='06021999')
    # cursor = connection.cursor()
    # cursor.execute("select NVDA_Value from testing")
    # result = cursor.fetchall()
    # for line in result :
    #     t= float(re.search(r'\d+', str(line)).group())
    #     TestingData.append(t)
    # print(TestingData)

    polo = Poloniex('QHKEQWBN-667F2YR6-QZ1WM5OX-VVB4GBSX', 'f7bc3077b4df19ffa9932253aeb329821b1377a2ba6c274b797f599e9ba555a5282fd032f539c416087dc5afcacade3fef6dd00f527910ed92a4c8be1ea13c15')
    # ForRealTime
    while(True):
        print(datetime.now().strftime("%H:%M:%S"))
        IsNextOperationBuy = not IsNextOperationBuy
        ticker = polo.returnTicker()['USDC_BTC']['last']
        # lowestAsk = polo.returnTicker()['USDC_BTC']['lowestAsk']
        balances = polo.returnBalances()['BTC']
        if IsNextOperationBuy == True :
            totalMain = []
            totalMain = tryToBuy(ticker,BalanceUSD,BalanceBTC)
            print(totalMain)
            # BalanceBTC = totalMain[0]
            # BalanceUSDT = totalMain[1]

        elif IsNextOperationBuy == False:
            totalMain = []
            print(ticker+BalanceUSD+BalanceBTC)
            totalMain = tryToSell(ticker,BalanceUSD,BalanceBTC)
            print(totalMain)
            BalanceBTC = totalMain[0]
            BalanceUSDT = totalMain[1]
        # totalMain = attemptToMakeTrade(IsNextOperationBuy,ticker,BalanceUSD,BalanceBTC,total) | as part of buying using thresholds
        # BalanceUSD = totalMain[0]
        # BalanceBTC = totalMain[1]
        # print('lastValue=', ticker)
        print('myBalance =', balances)
        print('usd=',totalMain[0])
        print('BTC=', totalMain[1],'\n')

        time.sleep(5)
    #ForTesting
        # for x in TestingData:
        #     IsNextOperationBuy = not IsNextOperationBuy
        #     if IsNextOperationBuy == True:
        #         totalMain = tryToBuy(ticker, BalanceUSD, BalanceBTC)
        #         BalanceBTC = totalMain[0]
        #         BalanceUSDT = totalMain[1]
        #
        #     elif IsNextOperationBuy == False:
        #         totalMain = tryToSell(ticker, BalanceUSD, BalanceBTC)
        #         BalanceBTC = totalMain[0]
        #         BalanceUSDT = totalMain[1]
        # Total = BalanceBTC * x + BalanceUSD
        # print(Total)





#
# BLUSD_B4 = BLUSD
#         BLUSD = BLUSD * ((100 - Sell_ROI*1.5) / 100)
#         BLBTC = BLBTC + (BLUSD_B4 - BLUSD)/BTC
#         B.append(BLUSD)
#         B.append(BLBTC)


