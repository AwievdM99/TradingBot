import time
from luno_python.client import Client
import random
def main():
    period = 0.1
    conn = Client(api_key_id='', api_key_secret='') 
    phase = 0
    trades = 319
    print(trades)
    while True:
        try:
            time.sleep(period)
            res = conn.get_ticker(pair='ETHZAR')
            buy = res['bid'][:-9]
            sell = res['ask'][:-9]
            spread = int(sell) - int(buy)
            buyPrice = int(buy)+1
            amount = 30/buyPrice
            amount = amount//0.000001/1000000
            sellPrice = 30.03/amount
            sellPrice = str(sellPrice).split(".")
            sellPrice = sellPrice[0]
            sellPrice = str(sellPrice).split(".")
            sellPrice = sellPrice[0]
            randomlist = []
            for i in range(0,10):
                n = random.randint(0,9)
                randomlist.append(n)
            key = ""
            for i in range(0,9):
                key = key + str(randomlist[i])
            x = conn.get_balances('ZAR')
            y = x['balance'][0]['balance']
            y = y.split(".")
            y = y[0]
            time.sleep(period)
            if int(y) > 30:
                phase = 1;
            while phase == 1:
                if int(spread) < 60:
                    phase = 0
                    time.sleep(period)
                    break
                print('Phase 1')
                conn.post_limit_order(pair='ETHZAR', price = buyPrice, type = 'BID', volume = amount, client_order_id= key, post_only=True) 
                print('Buying @ ' + str(buyPrice))
                time.sleep(50)
                orderID = (conn.get_order_v3(client_order_id=key))['order_id']
                if ((conn.get_order_v3(key))['status']) == "PENDING":
                    conn.stop_order(orderID)
                    print('Canceled')
                    phase = 0
                    break
                if ((conn.get_order_v3(key))['status']) == "COMPLETE":         
                    phase = 2
                    break
            while phase == 2:
                print('Phase 2')
                conn.post_limit_order(pair='ETHZAR', price = sellPrice, type = 'ASK', volume = amount)
                print('Selling @ ' + str(sellPrice))
                phase = 0
                trades = trades + 1
                print('_____________________________________')
                print(trades)
                print('_____________________________________')
                break
        except Exception as e:
            print(e)       
main()