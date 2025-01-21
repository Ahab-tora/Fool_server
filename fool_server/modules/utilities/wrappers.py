import time

def launching_wrapper(func:function):
    def wrapper():
        print(f'Running {func.__name__}')
        start = time.time()
        func()
        end = time.time()
        print(f'Executed {func.__name__} in {end-start}s')
    return wrapper