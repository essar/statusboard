from gpiozero import CompositeOutputDevice
from ic.flipflop import SRFlipFlop
from ic.ic import build_input_pin, build_output_pin
from time import sleep


class IC74595(CompositeOutputDevice):

    def __init__(self, **kwargs):

        pin_factory = kwargs.pop('pin_factory', None)
        if pin_factory is None:
            if CompositeOutputDevice.pin_factory is None:
                CompositeOutputDevice.pin_factory = CompositeOutputDevice._default_pin_factory()
            self.pin_factory = CompositeOutputDevice.pin_factory
        else:
            self.pin_factory = pin_factory

        devices = {}

        # Build output pins

        # Output enable (active-low)
        build_input_pin('oe', kwargs, devices, self.pin_factory, active_high=False)
        # Storage register clock
        build_input_pin('rclk', kwargs, devices, self.pin_factory)
        # Serial data input
        build_input_pin('ser', kwargs, devices, self.pin_factory)
        # Shift register clock
        build_input_pin('srclk', kwargs, devices, self.pin_factory)
        # Shift register clear (active-low)
        build_input_pin('srclr', kwargs, devices, self.pin_factory, active_high=False)

        # Build input pins

        # Q1
        build_output_pin('q1', kwargs, devices, self.pin_factory)
        # Q2
        build_output_pin('q2', kwargs, devices, self.pin_factory)
        # Q3
        build_output_pin('q3', kwargs, devices, self.pin_factory)
        # Q4
        build_output_pin('q4', kwargs, devices, self.pin_factory)
        # Q5
        build_output_pin('q5', kwargs, devices, self.pin_factory)
        # Q6
        build_output_pin('q6', kwargs, devices, self.pin_factory)
        # Q7
        build_output_pin('q7', kwargs, devices, self.pin_factory)
        # Q8
        build_output_pin('q8', kwargs, devices, self.pin_factory)

        if kwargs:
            raise TypeError('IC74959.__init__() got unexpected keyword argument "%s"' % kwargs.popitem()[0])

        super(IC74595, self).__init__(
            **devices,
            pin_factory=pin_factory
        )

        self.value = 0

    def __repr__(self):
        return '<board.%s object>' % self.__class__.__name__

    # Second order methods

    def clear(self):
        if hasattr(self, 'srclr'):
            self.srclr.off()
            self.pulse_srclk()
            self.srclr.on()

    def disable_output(self):
        if hasattr(self, 'oe'):
            self.oe.off()

    def enable_output(self):
        if hasattr(self, 'oe'):
            self.oe.on()

    def pulse_rclk(self, duration=0):
        if hasattr(self, 'rclk'):
            self.rclk.on()
            sleep(duration / 1000)
            self.rclk.off()

    def pulse_srclk(self, duration=0):
        if hasattr(self, 'srclk'):
            self.srclk.on()
            sleep(duration / 1000)
            self.srclk.off()

    # Third order methods

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, _value=0):
        # Reject value more than a single byte
        if _value < 0x00 or _value > 0xFF:
            raise ValueError("Value out of bounds")

        new_value = _value

        for i in range(0, 8):
            # Set serial input to first bit (LSB) of data
            self.ser.value = (_value & 0x01)
            # Clock the data into the register
            self.pulse_srclk()
            # Move to next bit
            _value = _value >> 1

        # Clock the storage register
        self.pulse_rclk()

        # Store the value internally
        self._value = new_value


class IC74595Simulator:

    def __init__(self, ic):
        self.ic = ic

        # Set up shift registers
        self.r = [SRFlipFlop() for x in range(0, 8)]
        self.sr = [SRFlipFlop() for x in range(0, 8)]

        # Output control
        self.print_register = False
        self.print_latch = False

    def __enter__(self):
        srclk_pin = self.ic.srclk.pin
        if srclk_pin is not None:
            srclk_pin.edges = 'rising'
            srclk_pin.when_changed = self.srclk_rise

        rclk_pin = self.ic.rclk.pin
        if rclk_pin is not None:
            rclk_pin.edges = 'rising'
            rclk_pin.when_changed = self.rclk_rise

        print("%s running" % self.__class__.__name__)

        return self

    def __exit__(self, *args):
        print("%s finished" % self.__class__.__name__)

    def _clock_latches(self):
        [x.clock() for x in self.r]

    def _clock_registers(self):
        [x.clock() for x in self.sr]

    def rclk_rise(self, ticks, state):
        # Set each latch value to output of register
        for i in range(0, 8):
            self.r[i].set = self.sr[i].output

        # Clock all latches
        self._clock_latches()

        # Set outputs
        if hasattr(self.ic, 'q1'):
            self.ic.q1.value = self.r[0].output
        if hasattr(self.ic, 'q2'):
            self.ic.q2.value = self.r[1].output
        if hasattr(self.ic, 'q3'):
            self.ic.q3.value = self.r[2].output
        if hasattr(self.ic, 'q4'):
            self.ic.q4.value = self.r[3].output
        if hasattr(self.ic, 'q5'):
            self.ic.q5.value = self.r[4].output
        if hasattr(self.ic, 'q6'):
            self.ic.q6.value = self.r[5].output
        if hasattr(self.ic, 'q7'):
            self.ic.q7.value = self.r[6].output
        if hasattr(self.ic, 'q8'):
            self.ic.q8.value = self.r[7].output

        if self.print_latch:
            print("[%s] (%d) R clocked: values=%s" % (self.ic, ticks, self.latch_values()))

    def srclk_rise(self, ticks, state):
        srclr_value = self.ic.srclr.value if hasattr(self.ic, 'srclr') else 1

        # Push data through register from LSB to MSB
        self.sr[7].set = self.ic.ser.value & srclr_value
        self.sr[6].set = self.sr[7].output & srclr_value
        self.sr[5].set = self.sr[6].output & srclr_value
        self.sr[4].set = self.sr[5].output & srclr_value
        self.sr[3].set = self.sr[4].output & srclr_value
        self.sr[2].set = self.sr[3].output & srclr_value
        self.sr[1].set = self.sr[2].output & srclr_value
        self.sr[0].set = self.sr[1].output & srclr_value

        # Clock all registers
        self._clock_registers()

        if self.print_register:
            print("[%s] (%d) SR clocked: values=%s" % (self.ic, ticks, self.register_values()))

    def register_values(self):
        return [x.output for x in self.sr]

    def latch_values(self):
        oe = (not hasattr(self.ic, 'oe')) or self.ic.oe.value
        return [x.output & oe for x in self.r]
