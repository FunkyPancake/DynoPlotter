import logging
import math

import numpy as np

from src.parser import LogParser


class SignalProcessor:
    def __init__(self, logger: logging.Logger, parser: LogParser, labels: dict):
        self.rpm = []
        self.rpm_time_ticks = []
        self.time_label = labels['time']
        self.torque_label = labels['torque']
        self.rpm_label = labels['rpm']
        self.filter_freq = float(labels['filter'])
        self.cut_idx = 0
        self.logger = logger
        self.parser = parser

    def process_base(self):
        time = self.parser.get_data(self.time_label)
        self.rpm = self.parser.get_data(self.rpm_label)
        self.cut_idx = next(i for i, x in enumerate(self.rpm) if x > 5000)
        self.rpm = self.filter_signal(self.rpm)
        rpm = self.rpm * 2 * math.pi / 60
        tick_trg = time[0]

        for i, t in enumerate(time[:self.cut_idx]):
            if tick_trg <= t:
                tick_trg = tick_trg + 1000
                rpm_tick = self.rpm[i]
                if rpm_tick % 500 == 0:
                    rpm_tick += 1
                self.rpm_time_ticks.append(rpm_tick)

        # calculate max rpm
        # filter data

        # calc constant dtime rpm indexes

        # calc power
        torque = self.parser.get_data(self.torque_label)[:self.cut_idx]
        torque = self.filter_signal(torque)
        power = np.multiply(rpm, torque) / 1000
        return self.rpm, torque, power

    def process_signal(self, name):
        return self.rpm, self.filter_signal(self.parser.get_data(name))

    def get_rpm_time_ticks(self) -> []:
        return self.rpm_time_ticks

    def filter_signal(self, signal):

        sz = [signal[0]] * len(signal)
        for i, s in enumerate(signal):
            if i == 0:
                continue
            sz[i] = self.filter_freq * s + (1 - self.filter_freq) * sz[i - 1]
        return np.array(sz[:self.cut_idx])
