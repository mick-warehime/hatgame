import random


def add_random(request):
    print('got' + request)
    new_value = int(request.value) + random.randint(1, 10)
    response = {'value': new_value}
    print('returned' + response)
    return response
