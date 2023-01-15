import asyncio
import aioconsole
import keyboard
from pynput import keyboard

msgGlobal = ""

def runCommand(stdout, command: str):
    stdout.write(command)

def on_press(key):
    try:
        print('Alphanumeric key pressed: {0} '.format(key.char))
        msgGlobal = "press_" + format(key.char)
    except AttributeError:
        print('special key pressed: {0}'.format(key))

    return False

def on_release(key):
    print('Key released: {0}'.format(key))
    msgGlobal = "release_" + format(key.char)
    return False


async def countDiff():
    while True:
        print(1)
        await asyncio.sleep(1)


async def main():
    # Collect events until released
    with keyboard.Listener(
            on_press=on_press,
            on_release=on_release) as listener:
        listener.join()

if __name__ == "__main__":
    asyncio.run(main())