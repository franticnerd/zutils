import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator
import numpy as np


class Plotter:
    def __init__(self):
        font = {'family': 'serif', 'serif': 'Times New Roman', 'size': 36}
        plt.rc('font', **font)
        plt.rc('legend', **{'fontsize': 26})

    def plot_hist(self, x, num_bin, xlabel, output_file):
        plt.figure()
        w = np.ones_like(x) / float(len(x))  # weights for computing frequency
        plt.hist(x, num_bin, weights=w,  color='g')
        self._set_axis(xlabel, 'Frequency')
        plt.savefig(output_file, bbox_inches='tight', pad_inches=0.03)

    def plot_scatter(self, x, y, xlabel, ylabel, output_file):
        plt.figure()
        plt.plot(x, y, 'bo')
        self._set_axis(xlabel, ylabel)
        plt.savefig(output_file, bbox_inches='tight', pad_inches=0.03)

    def plot_line_point(self, x, y_list, name_list, xlabel, ylabel, output_file):
        plt.figure()
        options = ['bo-', 'rs--', 'kd:', 'm*-.']
        plot_list = []
        for i in xrange(len(y_list)):
            p, = plt.plot(x, y_list[i], options[i], lw=2, ms=14)
            plot_list.append(p)
        self._set_axis(xlabel, ylabel)
        plt.legend(plot_list, name_list, loc='best', numpoints=1)
        plt.savefig(output_file, bbox_inches='tight', pad_inches=0.03)

    def plot_bar(self, x, y_list, name_list, xlabel, ylabel, output_file):
        plt.figure()
        options = ['bo-', 'rs--', 'kd:', 'm*-.']
        plot_list = []
        for i in xrange(len(y_list)):
            p, = plt.plot(x, y_list[i], options[i], lw=2, ms=14)
            plot_list.append(p)
        self._set_axis(xlabel, ylabel)
        plt.legend(plot_list, name_list, loc='best', numpoints=1)
        plt.savefig(output_file, bbox_inches='tight', pad_inches=0.03)

    def _set_axis(self, xlabel, ylabel):
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        # set the maximum number of ticks
        plt.gca().get_xaxis().set_major_locator(MaxNLocator(5))
        plt.gca().get_yaxis().set_major_locator(MaxNLocator(5))

if __name__ == '__main__':
    x = np.array([2, 3, 5, 46, 7, 2, 4, 67, 7, 8, 6, 8, 1, -23, 42])
    y = np.array([2, 3, 5, 46, 7, 2, 4, 67, 7, 8, 6, 8, 1, -23, 42])
    plotter = Plotter()
    # plotter.plot_hist(x, 3, 'X', 'test.pdf')
    # plotter.plot_scatter(x, y, 'X', 'Y', 'test.pdf')
    x = np.array([2, 4, 6, 8, 10])
    y1 = np.array([3, 53, 2, 23, 12])
    y2 = np.array([8, 33, 2, 3, 72])
    y3 = np.array([7, 23, 2, 23, 12])
    y4 = np.array([2, 83, 3, 28, 22])
    plotter.plot_line_point(x, [y1, y2, y3, y4], ['1', '2', '3', '4'], 'X', 'Y', 'test.pdf')
