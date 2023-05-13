import random
import time
import numpy as np
import Controller.CommunicationController as Communicator
import Controller.AIController as Ai_controller

import Parameter.EngineParameters as params

current_engine_power = [0, 0, 0, 0, 0, 0]


def provide_stability():
    pass


def provide_depth():
    pass


def provide_balance():
    pass


def provide_all():
    provide_stability()
    provide_depth()
    provide_balance()


def PID():
    pass


def normalize_data(data):
    array_data = np.array(data)
    normalized_data = array_data / np.sum(array_data)
    # total_data = multiplied = list(np.multiply(numbers1, numbers2))
    return normalized_data


def rotate_random(start_time):
    end_time = start_time + random.randint(1,2)

    Communicator.send_data_to_engines(params.turn_right_vector * random.choice([-1, 1]))
    # while int(time.time()) < end_time:
    #     send_data_to_engines(stop_vector)


def go_forward():
    Communicator.send_data_to_engines(params.forward_vector)


def calculate_engines_power(input):

    y = Ai_controller.model.predict(input)
    print(y)
    return y


def stop_all_functions():
    return params.stop_vector


def select_vector(power_vector):
    index = abs(list(power_vector).index(max(power_vector)))
    if power_vector[index] > 0:
        sign = 1
    else:
        sign = - 1
    if index is 0:
        print(str(sign) + " Go Forward")
        return sign * params.forward_vector
    # if index is 1:
    #     print(str(sign) + " Go Right")
    #     return sign * params.right_vector
    if index is 2:
        print(str(sign) + " Turn  right")
        return sign * params.turn_right_vector
    if index is 3:
        print(" Go Down")
        return True
