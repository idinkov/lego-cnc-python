from curio import sleep, Queue
from bricknil import attach, start
from bricknil.hub import PoweredUpHub
from bricknil.hub import CPlusHub, PoweredUpRemote
from motor import TechnicControlPlusXL, TechnicControlPlusLargeMotor
from bricknil.sensor import InternalMotor, RemoteButtons, LED, Button
from bricknil.process import Process
from bricknil.const import Color
import logging
import keyboard

@attach(RemoteButtons, name='btns_right',  capabilities=['sense_press'])
@attach(RemoteButtons, name='btns_left',  capabilities=['sense_press'])
class Remote(PoweredUpRemote):
    async def btns_left_change(self):
        if self.btns_left.plus_pressed():
            await self.tell_robot.put('forward')
        elif self.btns_left.minus_pressed():
            await self.tell_robot.put('backward')
        else:
            await self.tell_robot.put('stop')

    async def btns_right_change(self):
        if self.btns_right.plus_pressed():
            await self.tell_robot.put('right')
        elif self.btns_right.minus_pressed():
            await self.tell_robot.put('left')
        else:
            await self.tell_robot.put('stop')

    async def run(self):
        self.message('Running')
        # Set the remote LED to green to show we're ready
        while True:
            await sleep(10)   # Keep the remote running

@attach(TechnicControlPlusXL, name='hand_vertical')
@attach(TechnicControlPlusLargeMotor, name='hand_orbital')
@attach(TechnicControlPlusLargeMotor, name='hand_position')
class Hand(CPlusHub):

    async def run(self):
        self.message("Running")
        speed = 60

        # Set the robot LED to green to show we're ready
        while True:
            msg = await self.listen_remote.get()
            await self.listen_remote.task_done()
            if msg == 'forward':
                self.message('going forward')
                await self.hand_vertical.set_speed(speed)
            elif msg == 'backward':
                self.message('going backward')
                await self.hand_vertical.set_speed(-speed)
            elif msg == 'stop':
                self.message('stop')
                await self.hand_vertical.set_speed(0)
                await self.hand_orbital.set_speed(0)
                await self.hand_position.set_speed(0)
            elif msg == 'left':
                self.message('left')
                await self.hand_position.set_speed(-speed)
                await self.hand_orbital.set_speed(speed)
            elif msg == 'right':
                self.message('right')
                await self.hand_position.set_speed(speed)
                await self.hand_orbital.set_speed(-speed)

@attach(TechnicControlPlusXL, name='rotate_hand')
class MainHub(CPlusHub):

    async def run(self):
        self.message("Running")
        speed = 60

        # Set the robot LED to green to show we're ready
        while True:
            msg = await self.listen_remote.get()
            await self.listen_remote.task_done()
            if msg == 'forward':
                self.message('going forward')
                await self.rotate_hand.set_speed(speed)
            elif msg == 'backward':
                self.message('going backward')
                await self.rotate_hand.set_speed(-speed)
            elif msg == 'stop':
                self.message('stop')
                await self.rotate_hand.set_speed(0)
            elif msg == 'left':
                self.message('left')
                #await self.hand_position.set_speed(-speed)
                #await self.hand_orbital.set_speed(speed)
            elif msg == 'right':
                self.message('right')
                #await self.hand_position.set_speed(speed)
                #await self.hand_orbital.set_speed(-speed)


async def system():
    #00001624-1212-efde-1623-785feabcd123
    remote = Remote('remote')
    hand = Hand('Hand')
    mainHub = MainHub('Hand')
    #platform = Platform('Platform')

    # Define a message passing queue from the remote to the robot
    remote.tell_robot = Queue()
    hand.listen_remote = remote.tell_robot
    mainHub.listen_remote = remote.tell_robot

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    start(system)