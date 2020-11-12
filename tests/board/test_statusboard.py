import unittest
from board.statusboard import *
from ic.IC74595 import IC74595Simulator
from gpiozero.pins.mock import MockFactory

pin_factory = MockFactory()


class TestStatusBoard(unittest.TestCase):

    def test_testcard_dance(self):
        with IC74595Simulator(ic) as sim:
            sim.print_latch = True
            testcard_dance()
            self.assertEqual(0, ic.value)

    def test_disable_leds(self):
        with IC74595Simulator(ic) as sim:
            sim.print_latch = True
            ic.value = 0xFF

            disable_leds(LED1_MASK)
            self.assertEqual(254, ic.value)

            disable_leds(LED2_MASK)
            self.assertEqual(252, ic.value)

            disable_leds(LED3_MASK + LED4_MASK)
            self.assertEqual(240, ic.value)

            disable_leds(LED8_MASK)
            self.assertEqual(112, ic.value)

    def test_enable_leds(self):
        with IC74595Simulator(ic) as sim:
            sim.print_latch = True
            ic.value = 0x00

            enable_leds(LED1_MASK)
            self.assertEqual(1, ic.value)

            enable_leds(LED2_MASK)
            self.assertEqual(3, ic.value)

            enable_leds(LED3_MASK + LED4_MASK)
            self.assertEqual(15, ic.value)

            enable_leds(LED8_MASK)
            self.assertEqual(143, ic.value)


if __name__ == '__main__':
    unittest.main()
