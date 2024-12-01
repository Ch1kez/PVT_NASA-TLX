# import random
# import time
#
#
# def run_pvt_test():
#     delay = random.uniform(2, 5)
#     time.sleep(delay)
#     start = time.time()
#     input("СТОП!")
#     reaction_time = time.time() - start
#     return reaction_time


import random
import time

def perform_pvt_test():
    delay = random.uniform(2, 5)
    time.sleep(delay)
    start_time = time.time()
    # Пользователь нажимает кнопку...
    reaction_time = time.time() - start_time
    return reaction_time
