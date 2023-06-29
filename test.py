from functools import wraps
from flask import Flask

app = Flask(__name__)


class Animal(object):
    def __init__(self):
        self.domain_id = '123'

    # @wraps
    def __call__(self, func):
        def wrapper(*args, **kwargs):
            print('working here')
            user_id = '123'
            if user_id != self.domain_id:
                raise ValueError('error')
            return func(*args, **kwargs)
        return wrapper


@app.route('/<algorithm>/', methods=['get'])
@Animal()
def test(algorithm):
    word = f'{algorithm} belongs to'
    return word

# @animal
# def test(name, kind):
#     word = f'{name} belongs to {kind}'
#     return word

if __name__ == '__main__':
    app.run(host='localhost', port=8080, debug=True)
    # A = test('cow', 'mammals')
    # print(type(test))
    # print(A)
