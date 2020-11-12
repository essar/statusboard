from gpiozero import InputDevice, OutputDevice


class ICInputPin(OutputDevice):
    def __init__(self, pin, **kwargs):
        super(ICInputPin, self).__init__(pin, **kwargs)

    def _fire_events(self, old_v, new_v):
        if old_v == new_v:
            # No change, no edge
            return

        if new_v == 1 and (self.pin.edges in ('both', 'rising')):
            # Rising edge
            self._fire_when_changed()
        if new_v == 0 and (self.pin.edges in ('both', 'falling')):
            # Falling edge
            self._fire_when_changed()

    def _fire_when_changed(self):
        if self.pin.when_changed is not None:
            self.pin.when_changed(self.pin_factory.ticks(), self.value)

    def off(self):
        v = self.value
        super(ICInputPin, self).off()
        self._fire_events(v, self.value)

    def on(self):
        v = self.value
        super(ICInputPin, self).on()
        self._fire_events(v, self.value)


class ICOutputPin(InputDevice):
    def __init__(self, pin, **kwargs):
        super(ICOutputPin, self).__init__(pin, **kwargs)


def build_input_pin(name, args_in, devices_out, pin_factory, **kwargs):
    p = args_in.pop(name, None)
    if p is not None:
        devices_out[name] = ICInputPin(p, pin_factory=pin_factory, **kwargs)


def build_output_pin(name, args_in, devices_out, pin_factory, **kwargs):
    p = args_in.pop(name, None)
    if p is not None:
        devices_out[name] = ICOutputPin(p, pin_factory=pin_factory, **kwargs)
