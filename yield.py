from inspect import getgeneratorstate
from functools import wraps
from collections import namedtuple


def simple_coroutine():
    print('started')
    x = yield
    print('received: {}'.format(x))


def simple_coro2(a):
    print('started: a={}'.format(a))
    b = yield a
    print('received b={}'.format(b))
    c = yield a + b
    print('received c={}'.format(c))


def averager():
    total = 0.0
    count = 0
    average = None
    while True:
        b = yield average
        total += b
        count += 1
        average = total/count


def coroutine(func):
    """预激活协程"""
    @wraps(func)
    def decorator(*args, **kwargs):
        gen = func(*args, **kwargs)
        next(gen)
        return gen
    return decorator


@coroutine
def averager2():
    total = 0.0
    count = 0
    average = None
    while True:
        b = yield average
        total += b
        count += 1
        average = total/count


class DemoException(Exception):
    pass


@coroutine
def demo_exc_handling():
    print('coroutine start')
    try:
        while True:
            try:
                x = yield
            except DemoException:
                print('DemoException handled.')
            else:
                print('received: x={}'.format(x))
    finally:
        print('coroutine ending')


# 子生成器
Result = namedtuple('Result', 'count average')
# @coroutine
def averager3():
    total = 0.0
    count = 0
    average = None
    while True:
        b = yield
        if b is None:
            break
        total += b
        count += 1
        average = total/count
    return Result(count, average)


# yield from表达式做的第一件事是，调用iter()，从中获取迭代器
# def gen():
#     yield from 'AB'
#     yield from range(1, 3)


# 委派生成器
def grouper(results, key):
    while True:
        results[key] = yield from averager3()

# 客户端代码
def main(data):
    result = {}
    for key, values in data.items():
        group = grouper(result, key)
        next(group)
        for value in values:
            group.send(value)
        group.send(None)
    print(result)


if __name__ == '__main__':

    data = {
        'girls;kg': [40.9, 38.5],
        'girls;m': [1.6, 1.51]
    }
    main(data)


    # print(list(gen()))

    coro_avg = averager3()
    coro_avg.send(10)
    coro_avg.send(30)
    try:
        coro_avg.send(None)
    except StopIteration as exc:
        result = exc.value
    print(result)



    exc_coro = demo_exc_handling()
    exc_coro.send(11)
    # 关闭协调
    # exc_coro.close()
    exc_coro.throw(DemoException)


    # 装饰器预激活协程
    coro_avg2 = averager2()
    print(getgeneratorstate(coro_avg2))
    coro_avg2.send(40)
    coro_avg2.send(50)
    coro_avg2.send('spam')
    coro_avg2.send(60)

    coro_avg = averager()
    next(coro_avg)

    coro_avg.send(10)
    coro_avg.send(30)
    coro_avg.send(5)
    # coro_avg.close()

    my_coro2 = simple_coro2(14)
    print(getgeneratorstate(my_coro2))
    next(my_coro2)

    print(getgeneratorstate(my_coro2))
    my_coro2.send(28)

    my_coro2.send(99)


    my_coro = simple_coroutine()

    # 预激活协程
    # next(my_coro)
    my_coro.send(None)

    # 接受调用方的数据
    my_coro.send(42)
