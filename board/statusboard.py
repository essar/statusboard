from argparse import ArgumentParser
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

# Handle command line arguments
argparser = ArgumentParser()
argparser.add_argument('--test', action='store_const', const=True, default=False, help='Run in testing mode')
cmdargs = vars(argparser.parse_args())

# Configure board
if cmdargs['test']:
    pin_factory = MockFactory()
    ic = IC74595(ser=SER_OUTPUT_PIN, srclk=SRCLK_OUTPUT_PIN, rclk=RCLK_OUTPUT_PIN, pin_factory=pin_factory)
else:
    ic = IC74595(ser=SER_OUTPUT_PIN, srclk=SRCLK_OUTPUT_PIN, rclk=RCLK_OUTPUT_PIN)


def disable_leds(pin_mask):
    ic.value = (ic.value & ~pin_mask)


def enable_leds(pin_mask):
    ic.value = (ic.value | pin_mask)


def get_leds():
    return {
        1: ic.value & LED1_MASK > 0,
        2: ic.value & LED2_MASK > 0,
        3: ic.value & LED3_MASK > 0,
        4: ic.value & LED4_MASK > 0,
        5: ic.value & LED5_MASK > 0,
        6: ic.value & LED6_MASK > 0,
        7: ic.value & LED7_MASK > 0,
        8: ic.value & LED8_MASK > 0
    }


def set_leds(leds):
    value = (leds[1] * LED1_MASK) + \
            (leds[2] * LED2_MASK) + \
            (leds[3] * LED3_MASK) + \
            (leds[4] * LED4_MASK) + \
            (leds[5] * LED5_MASK) + \
            (leds[6] * LED6_MASK) + \
            (leds[7] * LED7_MASK) + \
            (leds[8] * LED8_MASK)
    ic.value = value


def startup():
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


def test(speed=10):
    sleep_secs = (1 / speed)
    result = {}

    # Start empty
    ic.value = 0

    result[1] = True
    result[2] = True
    result[3] = True
    result[4] = True
    result[5] = True
    result[6] = True
    result[7] = True
    result[8] = True

    enable_leds(LED1_MASK)
    result[1] &= ic.value & LED1_MASK > 0
    result[1] &= ic.value == LED1_MASK
    sleep(sleep_secs)

    enable_leds(LED2_MASK)
    result[2] &= ic.value & LED2_MASK > 0
    result[2] &= ic.value == LED1_MASK + LED2_MASK
    sleep(sleep_secs)

    enable_leds(LED3_MASK)
    result[3] &= ic.value & LED3_MASK > 0
    result[3] &= ic.value == LED1_MASK + LED2_MASK + LED3_MASK
    sleep(sleep_secs)

    enable_leds(LED4_MASK)
    result[4] &= ic.value & LED4_MASK > 0
    result[4] &= ic.value == LED1_MASK + LED2_MASK + LED3_MASK + LED4_MASK
    sleep(sleep_secs)

    enable_leds(LED5_MASK)
    result[5] &= ic.value & LED5_MASK > 0
    result[5] &= ic.value == LED1_MASK + LED2_MASK + LED3_MASK + LED4_MASK + \
        LED5_MASK
    sleep(sleep_secs)

    enable_leds(LED6_MASK)
    result[6] &= ic.value & LED6_MASK > 0
    result[6] &= ic.value == LED1_MASK + LED2_MASK + LED3_MASK + LED4_MASK + \
        LED5_MASK + LED6_MASK
    sleep(sleep_secs)

    enable_leds(LED7_MASK)
    result[7] &= ic.value & LED7_MASK > 0
    result[7] &= ic.value == LED1_MASK + LED2_MASK + LED3_MASK + LED4_MASK + \
        LED5_MASK + LED6_MASK + LED7_MASK
    sleep(sleep_secs)

    enable_leds(LED8_MASK)
    result[8] &= ic.value & LED8_MASK > 0
    result[8] &= ic.value == LED1_MASK + LED2_MASK + LED3_MASK + LED4_MASK + \
        LED5_MASK + LED6_MASK + LED7_MASK + LED8_MASK
    sleep(sleep_secs)

    disable_leds(LED1_MASK)
    result[1] &= ic.value & LED1_MASK == 0
    result[1] &= ic.value == LED2_MASK + LED3_MASK + LED4_MASK + LED5_MASK + \
        LED6_MASK + LED7_MASK + LED8_MASK
    sleep(sleep_secs)

    disable_leds(LED2_MASK)
    result[2] &= ic.value & LED2_MASK == 0
    result[2] &= ic.value == LED3_MASK + LED4_MASK + LED5_MASK + LED6_MASK + \
        LED7_MASK + LED8_MASK
    sleep(sleep_secs)

    disable_leds(LED3_MASK)
    result[3] &= ic.value & LED3_MASK == 0
    result[3] &= ic.value == LED4_MASK + LED5_MASK + LED6_MASK + LED7_MASK + \
        LED8_MASK
    sleep(sleep_secs)

    disable_leds(LED4_MASK)
    result[4] &= ic.value & LED4_MASK == 0
    result[4] &= ic.value == LED5_MASK + LED6_MASK + LED7_MASK + LED8_MASK
    sleep(sleep_secs)

    disable_leds(LED5_MASK)
    result[5] &= ic.value & LED5_MASK == 0
    result[5] &= ic.value == LED6_MASK + LED7_MASK + LED8_MASK
    sleep(sleep_secs)

    disable_leds(LED6_MASK)
    result[6] &= ic.value & LED6_MASK == 0
    result[6] &= ic.value == LED7_MASK + LED8_MASK
    sleep(sleep_secs)

    disable_leds(LED7_MASK)
    result[7] &= ic.value & LED7_MASK == 0
    result[7] &= ic.value == LED8_MASK
    sleep(sleep_secs)

    disable_leds(LED8_MASK)
    result[8] &= ic.value & LED8_MASK == 0
    result[8] &= ic.value == 0
    sleep(sleep_secs)

    ic.value = 0

    return result


if not cmdargs['test']:
    # Run startup routine
    startup()
