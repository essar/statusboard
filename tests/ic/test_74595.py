import unittest
from gpiozero.pins.mock import MockFactory
from ic.IC74595 import IC74595, IC74595Simulator

pin_factory = MockFactory()


class TestIC(unittest.TestCase):

    def test_create(self):
        print('--------------------------------')
        print('test_create')
        print('--------------------------------')
        with IC74595(ser=1, srclk=2, srclr=3, rclk=4, oe=5, pin_factory=pin_factory) as ic:
            ic.oe.on()
            print(super(IC74595, ic).value)

            self.assertEqual(0, ic.ser.value)

    def test_value_exceeds_max_bounds(self):
        print('--------------------------------')
        print('test_value_exceeds_max_bounds')
        print('--------------------------------')
        with IC74595(ser=1, srclk=2, srclr=3, rclk=4, oe=5, pin_factory=pin_factory) as ic:
            print(super(IC74595, ic).value)
            with self.assertRaises(ValueError):
                ic.value = 0x100

    def test_value_exceeds_min_bounds(self):
        print('--------------------------------')
        print('test_value_exceeds_min_bounds')
        print('--------------------------------')
        with IC74595(ser=1, srclk=2, srclr=3, rclk=4, oe=5, pin_factory=pin_factory) as ic:
            print(super(IC74595, ic).value)
            with self.assertRaises(ValueError):
                ic.value = -0x01

    def test_value_zero(self):
        print('--------------------------------')
        print('test_value_zero')
        print('--------------------------------')
        with IC74595(ser=1, srclk=2, srclr=3, rclk=4, oe=5, pin_factory=pin_factory) as ic:
            ic.oe.on()
            ic.srclr.on()
            print(super(IC74595, ic).value)
            with IC74595Simulator(ic) as sim:
                ic.value = 0x00
                self.assertEqual([0, 0, 0, 0, 0, 0, 0, 0], sim.register_values())
                self.assertEqual([0, 0, 0, 0, 0, 0, 0, 0], sim.latch_values())

    def test_value_zero_without_srclr(self):
        print('--------------------------------')
        print('test_value_zero_without_srclr')
        print('--------------------------------')
        with IC74595(ser=1, srclk=2, rclk=4, oe=5, pin_factory=pin_factory) as ic:
            ic.oe.on()
            print(super(IC74595, ic).value)
            with IC74595Simulator(ic) as sim:
                ic.value = 0x00
                self.assertEqual([0, 0, 0, 0, 0, 0, 0, 0], sim.register_values())
                self.assertEqual([0, 0, 0, 0, 0, 0, 0, 0], sim.latch_values())

    def test_value_one_bit(self):
        print('--------------------------------')
        print('test_value_one_bit')
        print('--------------------------------')
        with IC74595(ser=1, srclk=2, srclr=3, rclk=4, oe=5, pin_factory=pin_factory) as ic:
            ic.oe.on()
            ic.srclr.on()
            print(super(IC74595, ic).value)
            with IC74595Simulator(ic) as sim:
                ic.value = 0x01
                self.assertEqual([1, 0, 0, 0, 0, 0, 0, 0], sim.register_values())
                self.assertEqual([1, 0, 0, 0, 0, 0, 0, 0], sim.latch_values())

    def test_value_two_bits(self):
        print('--------------------------------')
        print('test_value_two_bits')
        print('--------------------------------')
        with IC74595(ser=1, srclk=2, srclr=3, rclk=4, oe=5, pin_factory=pin_factory) as ic:
            ic.oe.on()
            ic.srclr.on()
            print(super(IC74595, ic).value)
            with IC74595Simulator(ic) as sim:
                ic.value = 0x81
                self.assertEqual([1, 0, 0, 0, 0, 0, 0, 1], sim.register_values())
                self.assertEqual([1, 0, 0, 0, 0, 0, 0, 1], sim.latch_values())

    def test_value_all_bits(self):
        print('--------------------------------')
        print('test_value_two_bits')
        print('--------------------------------')
        with IC74595(ser=1, srclk=2, srclr=3, rclk=4, oe=5, pin_factory=pin_factory) as ic:
            ic.oe.on()
            ic.srclr.on()
            print(super(IC74595, ic).value)
            with IC74595Simulator(ic) as sim:
                ic.value = 0xFF
                self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1], sim.register_values())
                self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1], sim.latch_values())

    def test_disable_output(self):
        print('--------------------------------')
        print('test_disable_output')
        print('--------------------------------')
        with IC74595(ser=1, srclk=2, srclr=3, rclk=4, oe=5, pin_factory=pin_factory) as ic:
            ic.oe.on()
            ic.srclr.on()
            print(super(IC74595, ic).value)
            with IC74595Simulator(ic) as sim:
                ic.disable_output()
                ic.value = 0xFF
                self.assertEqual([0, 0, 0, 0, 0, 0, 0, 0], sim.latch_values())

    def test_enable_output(self):
        print('--------------------------------')
        print('test_enable_output')
        print('--------------------------------')
        with IC74595(ser=1, srclk=2, srclr=3, rclk=4, oe=5, pin_factory=pin_factory) as ic:
            ic.oe.off()
            ic.srclr.on()
            print(super(IC74595, ic).value)
            with IC74595Simulator(ic) as sim:
                ic.enable_output()
                ic.value = 0xFF
                self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1], sim.latch_values())

    def test_clear_and_clock(self):
        print('--------------------------------')
        print('test_clear_and_clock')
        print('--------------------------------')
        with IC74595(ser=1, srclk=2, srclr=3, rclk=4, oe=5, pin_factory=pin_factory) as ic:
            ic.oe.off()
            ic.srclr.on()
            print(super(IC74595, ic).value)
            with IC74595Simulator(ic) as sim:
                ic.value = 0xFF
                self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1], sim.register_values())
                ic.srclr.off()
                ic.pulse_srclk()
                self.assertEqual([0, 0, 0, 0, 0, 0, 0, 0], sim.register_values())

    def test_clear(self):
        print('--------------------------------')
        print('test_clear')
        print('--------------------------------')
        with IC74595(ser=1, srclk=2, srclr=3, rclk=4, oe=5, pin_factory=pin_factory) as ic:
            ic.oe.on()
            ic.srclr.on()
            print(super(IC74595, ic).value)
            with IC74595Simulator(ic) as sim:
                ic.value = 0xFF
                self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1], sim.register_values())
                ic.clear()
                self.assertEqual([0, 0, 0, 0, 0, 0, 0, 0], sim.register_values())
                self.assertEqual([1, 1, 1, 1, 1, 1, 1, 1], sim.latch_values())
