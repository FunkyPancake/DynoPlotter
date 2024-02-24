import matplotlib.pyplot as plt
import numpy as np
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg
from matplotlib.offsetbox import AnchoredText


class CustomPlot(FigureCanvasQTAgg):

    def __init__(self):
        self.ax_dict = {}
        fig, ax1 = plt.subplots()
        plt.grid(visible=True, which='both')
        self.fig = fig
        self.ax1 = ax1
        # plt.legend(loc="upper left")
        # fig = Figure(figsize=(width, height), dpi=dpi)
        # self.axes = fig.add_subplot(111)
        self.fig.subplots_adjust(top=0.99,bottom=0.1)
        super(CustomPlot, self).__init__(fig)

    def add_plot(self, name, x, y, label=None):
        ax = self.ax1.twinx()
        self.ax_dict[name] = ax
        self.fig.subplots_adjust(right=0.9 - (len(self.ax_dict) * 0.1))
        if label is None:
            label = name
        color = (np.random.random(), np.random.random(), np.random.random())
        ax.set_ylabel(label, color=color)
        ax.plot(x, y, c=color, label=label)
        ax.spines.right.set_position(('outward', 50 + 50 * (len(self.ax_dict) - 1)))
        self.draw()

    def delete_plot(self, name):
        plot = self.ax_dict.pop(name)
        plot.cla()
        plot.remove()
        self.fig.subplots_adjust(right=0.9 - (len(self.ax_dict) * 0.1))
        self.draw()

    def add_base_plots(self, rpm, torque, power):
        self.fig.subplots_adjust(left=0.09)
        self.ax1.plot(rpm, torque, 'g-')
        self.ax1.set_xlabel('RPM')
        self.ax1.set_ylabel('Torque [Nm]', color='g')

        ax = self.ax1.twinx()
        ax.plot(rpm, power, 'r-')
        ax.set_ylabel('Power [kW]', color='r')
        self.draw()
        at = AnchoredText(
            f"{max(power):.0f} kW @ {rpm[np.argmax(power)]:.0f} rpm" +
            f"\n{max(torque):.0f} Nm @ {rpm[np.argmax(torque)]:.0f} rpm",
            prop=dict(size=15), frameon=True, loc='upper left')
        at.patch.set_boxstyle("round,pad=0.,rounding_size=0.2")
        self.ax1.add_artist(at)
