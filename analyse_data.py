#!/usr/bin/python3
# coding: utf8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from numpy import random


def load_data():
    return pd.read_csv('docum.txt')

def variance(xs):
    '''Вычисление корреляции,
       несмещенная дисперсия при n <= 30'''
    x_hat = xs.mean()
    n = xs.count()
    n = n - 1 if n in range( 1, 30 ) else n
    return sum((xs - x_hat) ** 2) / n

def standard_deviation(xs):
    '''Вычисление стандартного отклонения'''
    return np.sqrt(variance(xs))

def covariance(xs, ys):
    '''Вычисление ковариации (несмещенная, т.е. n-1)'''
    dx = xs - xs.mean()
    dy = ys - ys.mean()
    return (dx * dy).sum() / (dx.count() - 1)

def correlation(xs, ys):
    '''Вычисление корреляции'''
    return covariance(xs, ys) / (standard_deviation(xs) *
                                 standard_deviation(ys))

def jitter(limit):
    '''Генератор джиттера (произвольного сдвига точек данных)'''
    return lambda x: random.uniform(-limit, limit) + x

def slope(xs, ys):
    return xs.cov(ys) / xs.var()

def intercept(xs, ys):
    print(f"{xs.mean()}")
    print(f"{slope(xs,ys)}")
    return ys.mean() - (xs.mean() * slope(xs, ys))

'''Функция линии регрессии'''
regression_line = lambda a, b: lambda x: a + (b * x)  # вызовы fn(a,b)(x)

def residuals(a, b, xs, ys):
    '''Вычисление остатков'''
    estimate = regression_line(a, b)     # частичное применение
    return pd.Series( map(lambda x, y: y - estimate(x), xs, ys) )

def ex_3_2():
    '''Визуализация разброса значений
       роста спортсменов на гистограмме'''
    df = load_data()
    xs = df['btcusdt']
    ys = df['ethusdt']
    print(f"correlation {correlation(xs,ys)} count {len(xs)}")
    a = intercept(xs, ys)
    b = slope(xs, ys)
    print(f"a = {a} b = {b}")
    pd.DataFrame(np.array([xs, ys]).T).plot.scatter(0, 1, s=12, grid=True)
    plt.xlabel('BTCUSDT')
    plt.ylabel('ETHUSDT')
    plt.show()

constantly = lambda x: 0

def r_squared(a, b, xs, ys):
    '''Рассчитать коэффициент детерминации (R-квадрат)'''
    r_var = residuals(a, b, xs, ys).var()
    y_var = ys.var()
    return 1 - (r_var / y_var)

def ex_3_14():
    '''Построение графика остатков на примере данных роста и веса'''
    df = load_data()
    xs = df['btcusdt']
    ys = df['ethusdt']
    a = intercept(xs, ys)
    b = slope(xs, ys)
    min_btc = int(xs.min())
    max_btc = int(xs.max())
    print(f"{min_btc} {max_btc}")
    print(f"a = {a} b = {b} xs.mean = {(min_btc+max_btc)/2.0}")
    print(f"rsquared = {r_squared(a, b, xs, ys)}")
    y = residuals(a, b, xs, ys)
    ax = pd.DataFrame(np.array([xs, y]).T).plot.scatter(0, 1, s=12)
    s = pd.Series(range(min_btc, max_btc))
    df = pd.DataFrame( {0:s, 1:s.map(constantly)} )
    df.plot(0, 1, legend=False, grid=True, ax=ax)
    plt.xlabel('btcusdt')
    plt.ylabel('ethusdt')
    plt.show()

if __name__ == '__main__':
    ex_3_2()
    ex_3_14()