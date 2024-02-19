import math

import numpy as np


class SignalProcessor:
    def __init__(self, logger, parser):
        self.logger = logger
        self.parser = parser

    def calc_power(self):
        rpm = self.parser.get_data('STAT_MOTORDREHZAHL_WERT') * 2 * math.pi / 60
        torque = self.parser.get_data('STAT_MOTORMOMENT_AKTUELL_WERT')
        power = np.multiply(rpm, torque) / 1000

        if power is None:
            return []
        return power
