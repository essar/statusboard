from board.config import config
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

led_map = {
    1: LED1_MASK,
    2: LED2_MASK,
    3: LED3_MASK,
    4: LED4_MASK,
    5: LED5_MASK,
    6: LED6_MASK,
    7: LED7_MASK,
    8: LED8_MASK
}

# Configure board
if config.test_mode:
    pin_factory = MockFactory()
    ic = IC74595(ser=SER_OUTPUT_PIN, srclk=SRCLK_OUTPUT_PIN, rclk=RCLK_OUTPUT_PIN, pin_factory=pin_factory)
else:
    ic = IC74595(ser=SER_OUTPUT_PIN, srclk=SRCLK_OUTPUT_PIN, rclk=RCLK_OUTPUT_PIN)


def disable_leds(pin_mask):
    ic.value = (ic.value & ~pin_mask)


def enable_leds(pin_mask):
    ic.value = (ic.value | pin_mask)


def get_leds():
    return {k: 1 if ic.value & led_map[k] > 0 else 0 for k in led_map.keys()}


def set_leds(leds, merge=False):
    if merge:
        current = get_leds()
        ic.value = sum([(1 if (leds[k] if k in leds else current[k]) > 0 else 0) * led_map[k] for k in led_map.keys()])
    else:
        ic.value = sum([(1 if leds[k] > 0 else 0) * led_map[k] for k in led_map.keys()])


def reset():
    ic.value = 0


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

    # Store starting value
    start_value = ic.value

    # Reset
    reset()

    # Create result dict
    result = {k: True for k in led_map.keys()}

    for i in led_map.keys():
        enable_leds(led_map[i])
        result[i] &= ic.value & led_map[i] > 0
        result[i] &= ic.value == sum([led_map[k] for k in led_map.keys() if k <= i])
        sleep(sleep_secs)

    for i in led_map.keys():
        disable_leds(led_map[i])
        result[i] &= ic.value & led_map[i] == 0
        result[i] &= ic.value == sum([led_map[k] for k in led_map.keys() if k > i])
        sleep(sleep_secs)

    # Reset to original value
    ic.value = start_value

    return {k: ('OK' if result[k] else 'FAIL') for k in result.keys()}


if not config.test_mode:
    # Run startup routine
    startup()
