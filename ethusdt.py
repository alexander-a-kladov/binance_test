#!/usr/bin/python3
# coding: utf8

import json, requests, time, math
from collections import deque
from math_func import linear_regression, get_line_value
import threading

binance_api = 'https://api.binance.com/api/v3/ticker/price?symbol='

btcd = deque()
ethd = deque()
timed = deque()

slope = 0
intercept = 0
lock = 0

def append_data(price_eth, price_btc, time_sec):
    global btcd, ethd, timed
    lock.acquire()
    btcd.append(price_btc)
    ethd.append(price_eth)
    lock.release()
    timed.append(time_sec)

def get_data(index: int)->(float,float,float):
    global btcd, ethd, timed
    return ethd[index], btcd[index], timed[index]

def pop_data_left():
    global btcd, ethd, timed
    lock.acquire()
    price_eth = ethd.popleft()
    price_btc = btcd.popleft()
    lock.release()
    time_sec = timed.popleft()
    return price_eth, price_btc, time_sec

def get_own_eth_move(price_eth, price_btc, new_price_eth, new_price_btc):
    lock.acquire()
    price_eth -= get_line_value(price_btc, slope, intercept)
    new_price_eth -= get_line_value(new_price_btc, slope, intercept)
    lock.release()
    return new_price_eth-price_eth

def get_price(token: str):
    try:
        r = requests.get(binance_api+token)
        if r.status_code != 404:
            return float(json.loads(r.text).get('price'))
        else:
            return None
    except:
        print("Error connection")
        return None

def get_prices_and_time():
    price_eth = get_price('ETHUSDT')
    price_btc = get_price('BTCUSDT')
    time_sec = time.time()
    return time_sec, price_eth, price_btc

def calc_regression():
    global ethd, btcd, slope, intercept, lock
    time0 = time.time()
    lock.acquire()
    ethl = [*ethd]
    btcl = [*btcd]
    lock.release()
    slope_new, intercept_new = linear_regression(btcl, ethl)
    lock.acquire()
    slope = slope_new
    intercept = intercept_new
    lock.release()
    print(f"{slope} {intercept} {len(ethl)} {time.time()-time0}")
    price_eth, price_btc, time_sec = get_data(0)
    new_price_eth, new_price_btc, new_time = get_data(-1)
    own_eth_move = get_own_eth_move(price_eth, price_btc, new_price_eth, new_price_btc)
    print(f"{own_eth_move}")
    threading.Timer(60.0, calc_regression).start()

def start_regression():
    global lock
    lock = threading.Lock()
    threading.Timer(60.0, calc_regression).start()

def check_threshold_and_remove_old(move, delta_sec):
    global  ethd, btcd, timed
    price_eth, price_btc, time_sec = get_data(0)
    new_price_eth, new_price_btc, new_time = get_data(len(ethd)-1)
    while time_sec+delta_sec < new_time:
        price_eth, price_btc, time_sec = pop_data_left()
    own_eth_move = get_own_eth_move(price_eth, price_btc, new_price_eth, new_price_btc)
    if math.fabs(own_eth_move/price_eth) > move:
        print(f"eth_move {own_eth_move/price_eth} more than threshold {move*100}% delta {new_time - time_sec} sec")

def document_data(t, eth, btc):
    f = open("docum.txt", "a")
    if f:
        f.write(f"{t},{eth},{btc}\n")
        f.close()


if __name__ == '__main__':
    time_sec, prev_eth, prev_btc = get_prices_and_time()
    start_regression()
    if prev_eth and prev_btc:
        append_data(prev_eth, prev_btc, time_sec)
        #document_data(time_sec, prev_eth, prev_btc)
    while 1:
        new_time, price_eth, price_btc = get_prices_and_time()
        if price_btc and price_eth:
            append_data(price_eth, price_btc, new_time)
            #document_data(new_time, price_eth, price_btc)
        check_threshold_and_remove_old(0.01, 3600)
