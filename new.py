from curio import sleep, Queue
from bricknil import attach, start
from bricknil.hub import PoweredUpHub
from bricknil.hub import CPlusHub, PoweredUpRemote
from motor import TechnicControlPlusXL, TechnicControlPlusLargeMotor
from bricknil.sensor import InternalMotor, RemoteButtons, LED, Button
from bricknil.process import Process
from bricknil.const import Color
import logging
from pynput import keyboard

msgGlobal = ""

@attach(TechnicControlPlusXL, name='steering')
@attach(TechnicControlPlusLargeMotor, name='thrust')
@attach(TechnicControlPlusLargeMotor, name='rotate')
class MainHub(CPlusHub):
    global msgGlobal
    async def run(self):
        self.message("Running")
        speed = 60

        # Set the robot LED to green to show we're ready
        while True:

            with keyboard.Listener(
                    on_press=on_press,
                    on_release=on_release) as listener:
                listener.join()
            if msgGlobal == 'press_w':
                self.message('forward')
                await self.thrust.set_speed(speed)
            elif msgGlobal == 'press_s':
                self.message('backward')
                await self.thrust.set_speed(-speed)
            elif msgGlobal == 'release_w' or msgGlobal == 'release_s':
                self.message('stop')
                await self.thrust.set_speed(0)
            elif msgGlobal == 'press_a':
                self.message('left')
                #await self.steering.set_speed(-speed)
            elif msgGlobal == 'press_d':
                self.message('right')
                #await self.steering.set_speed(speed)


def on_press(key):
    global msgGlobal
    try:
        print('Alphanumeric key pressed: {0} '.format(key.char))
        msgGlobal = "press_" + format(key.char)
    except AttributeError:
        print('special key pressed: {0}'.format(key))

    if format(key.char) == "w":
        return False

    if format(key.char) == "s":
        return False

    return True

def on_release(key):
    global msgGlobal
    print('Key released: {0}'.format(key))
    msgGlobal = "release_" + format(key.char)
    if format(key.char) == "w":
        return False

    if format(key.char) == "s":
        return False

    return True


class VirtualRemote():
    def __init__(self):
        self.tell_robot = ""

    async def run(self):
        with keyboard.Listener(
                on_press=on_press,
                on_release=on_release) as listener:
            listener.join()
        await self.tell_robot.put("forward")

async def system():
    #00001624-1212-efde-1623-785feabcd123
    remote = VirtualRemote()
    main = MainHub('Main')

    # Define a message passing queue from the remote to the robot
    remote.tell_robot = Queue()
    main.listen_remote = remote.tell_robot

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start(system)
