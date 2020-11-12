from ic.IC74595 import IC74595
from time import sleep

from gpiozero.pins.mock import MockFactory

SER_OUTPUT_PIN = 22
SRCLK_OUTPUT_PIN = 17
RCLK_OUTPUT_PIN = 27

LED1_MASK = 0x01
LED2_MASK = 0x02
LED3_MASK = 0x04
LED4_MASK = 0x08
LED5_MASK = 0x10
LED6_MASK = 0x20
LED7_MASK = 0x40
LED8_MASK = 0x80

pin_factory = MockFactory()

# Configure board
# ic = IC74595(ser=SER_OUTPUT_PIN, srclk=SRCLK_OUTPUT_PIN, rclk=RCLK_OUTPUT_PIN, pin_factory=pin_factory)
ic = IC74595(ser=SER_OUTPUT_PIN, srclk=SRCLK_OUTPUT_PIN, rclk=RCLK_OUTPUT_PIN)


def disable_leds(pin_mask):
    ic.value = (ic.value & ~pin_mask)


def enable_leds(pin_mask):
    ic.value = (ic.value | pin_mask)


def test():
    """ Dance all the LEDs in a sequence for testing. """
    speed = 4
    sleep_secs = (1 / speed)

    # May not need this as will be wired low anyway, but here for completeness
    ic.enable_output()

    # Left to right
    for x in range(0, 8):
        ic.value = (2 ** x)
        sleep(sleep_secs)

    ic.value = 0
    sleep(sleep_secs)

    # Right to left
    for x in range(0, 8):
        ic.value = (2 ** (7 - x))
        sleep(sleep_secs)

    ic.value = 0
    sleep(sleep_secs)

    # Outside in
    for x in range(0, 4):
        ic.value = (2 ** x) + (2 ** (7 - x))
        sleep(sleep_secs)

    ic.value = 0
    sleep(sleep_secs)

    # Inside out
    for x in range(0, 4):
        ic.value = (2 ** (3 - x)) + (2 ** (4 + x))
        sleep(sleep_secs)

    ic.value = 0
    sleep(sleep_secs)

    # Double flash
    for x in range(0, 2):
        ic.value = 0xFF
        sleep(sleep_secs)
        ic.value = 0x00
        sleep(sleep_secs)

    # Finish blank
    ic.value = 0


if __name__ == '__main__':
    test()
