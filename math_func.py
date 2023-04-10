from functools import reduce

def mean(a: list)->float:
    return reduce(lambda x, y: x + y, a) / len(a)

def linear_regression(x: list, y: list)->float:
    sum1 = 0.0
    sum2 = 0.0
    mean_x = mean(x)
    mean_y = mean(y)
    for i in range(len(x)):
        sum1 += (x[i]-mean_x)*(y[i]-mean_y)
        sum2 += (x[i]-mean_x)*(x[i]-mean_x)
    try:
        slope = sum1/sum2
        intercept = mean_y - mean_x*slope
    except:
        slope = 0
        intercept = 0
    return slope, intercept

def get_line_value(x, slope, intercept)->float:
    return x*slope+intercept
