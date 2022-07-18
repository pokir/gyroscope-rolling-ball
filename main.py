from math import floor
import os
from time import sleep


def init_gyro():
    os.system('termux-sensor -s rotation_vector -d 50 > output.txt &')


def get_gyro():
    with open('output.txt', 'r') as f:
        data = f.readlines()[-7:-4]

        try:
            data = list(map(lambda s: float(s.strip().replace(',', '')), data))
        except ValueError:
            return None

        if len(data) != 3:
            return None

        return data


if __name__ == '__main__':
    init_gyro()

    dim = os.get_terminal_size()

    data = None

    vel_x = 0
    vel_y = 0

    pos_x = dim.columns / 2
    pos_y = dim.lines / 2

    while True:
        # display world
        dim = os.get_terminal_size() # get the size again in case terminal resized
        buffer = ''

        for y in range(dim.lines):
            for x in range(dim.columns):
                if x == floor(pos_x) and y == floor(pos_y):
                    buffer += 'O'
                elif 0 in [x, y] or x == dim.columns - 1 or y == dim.lines - 1:
                    buffer += 'M'
                else:
                    buffer += ' '

        print(buffer, end='')

        sleep(0.02)

        # update rotation data
        new_data = get_gyro()

        # if the new data hasn't been read properly, do nothing and use the old data
        if new_data is not None:
            data = new_data

        # if data hasn't been updated yet, retry
        if data is None: continue 

        # reset acceleration
        acc_x = 0
        acc_y = 0

        # add forces
        x_rot, y_rot, z_rot = data

        vertical_component = x_rot * 0.5
        horizontal_component = y_rot * 0.5

        acc_x += horizontal_component
        acc_y += vertical_component

        acc_x -= vel_x * 0.1
        acc_y -= vel_y * 0.1

        # apply acceleration
        vel_x += acc_x
        vel_y += acc_y

        # collisions
        if pos_x + vel_x < 1 or pos_x + vel_x > dim.columns - 1:
            vel_x *= -1

        if pos_y + vel_y < 1 or pos_y + vel_y > dim.lines - 1:
            vel_y *= -1

        # apply velocity
        pos_x += vel_x
        pos_y += vel_y
