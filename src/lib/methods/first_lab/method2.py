import numpy as np
from scipy import signal
import matplotlib.backends.backend_qtagg as matplotlib_backend_qtagg
import matplotlib.figure as matplotlib_figure
import lib.methods.first_lab.models as methods_first_lab_models


class MplCanvas(matplotlib_backend_qtagg.FigureCanvasQTAgg):
    def __init__(
        self, w, a, w2, a2, width=8, height=6, dpi=100,
    ):
        self.w = w
        self.a = a
        self.w2 = w2
        self.a2 = a2

        plt_ = matplotlib_figure.Figure(figsize=(width, height), dpi=dpi)
        plt_.tight_layout()
        plt_.subplots_adjust(hspace=0.5, wspace=0.3)

        self.axes = plt_.add_subplot(3, 2, 1)
        t, y = signal.step(w)
        self.axes.plot(t, y, label='w', color='blue')  # Указываем цвет синий для w
        t, y = signal.step(w2)
        self.axes.plot(t, y, label='w2', color='red')  # Указываем цвет красный для w2
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('Step Response')
        self.axes.set_title('Step Response')
        self.axes.grid(True)
        self.axes.legend()

        # Impulse Response
        self.axes = plt_.add_subplot(3, 2, 2)
        t, y = signal.impulse(w)
        self.axes.plot(t, y, label='w', color='blue')
        t, y = signal.impulse(w2)
        self.axes.plot(t, y, label='w2', color='red')
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('Impulse Response')
        self.axes.set_title('Impulse Response')
        self.axes.grid(True)
        self.axes.legend()

        # Bode Plot - Magnitude
        self.axes = plt_.add_subplot(3, 2, 3)
        w_, mag, phase = signal.bode(w)
        self.axes.semilogx(w_, mag, label='w', color='blue')
        w_, mag, phase = signal.bode(w2)
        self.axes.semilogx(w_, mag, label='w2', color='red')
        self.axes.set_xlabel('Frequency')
        self.axes.set_ylabel('Magnitude (dB)')
        self.axes.set_title('Bode Plot - Magnitude')
        self.axes.grid(True)
        self.axes.legend()

        # Bode Plot - Phase
        self.axes = plt_.add_subplot(3, 2, 4)
        # w, phase = signal.bode(w)
        self.axes.semilogx(w_, phase, label='w', color='blue')
        # w, phase = signal.bode(w2)
        self.axes.semilogx(w_, phase, label='w2', color='red')
        self.axes.set_xlabel('Frequency')
        self.axes.set_ylabel('Phase (degrees)')
        self.axes.set_title('Bode Plot - Phase')
        self.axes.grid(True)
        self.axes.legend()

        # Nyquist Plot
        self.axes = plt_.add_subplot(3, 2, 5)
        w_, h = signal.freqresp(w)
        self.axes.plot(h.real, h.imag, label='w', color='blue')
        w_, h = signal.freqresp(w2)
        self.axes.plot(h.real, h.imag, label='w2', color='red')
        self.axes.set_xlabel('Real')
        self.axes.set_ylabel('Imaginary')
        self.axes.set_title('Nyquist Plot')
        self.axes.grid(True)
        self.axes.legend()

        # Pole-Zero Map
        self.axes = plt_.add_subplot(3, 2, 6)
        poles = np.roots(a)
        self.axes.plot(poles.real, poles.imag, 'x', label='w', color='blue')
        poles = np.roots(a2)
        self.axes.plot(poles.real, poles.imag, 'x', label='w2', color='red')
        self.axes.set_xlabel('Real')
        self.axes.set_ylabel('Imaginary')
        self.axes.set_title('Pole-Zero Map')
        self.axes.grid(True)
        self.axes.legend()

        super(MplCanvas, self).__init__(plt_)

    def get_copy(self):
        return MplCanvas(self.w, self.a, self.w2, self.a2)


def calculate_method(request: methods_first_lab_models.FirstLabModel):
    b_n_a2 = [
        ([2 * request.k], [request.t ** 2, 2 * request.t * request.xi, 1]),
        ([request.k], [(2 * request.t) ** 2, 2 * 2 * request.t * request.xi, 1]),
        ([request.k], [request.t ** 2, 2 * request.t * (0.5 * request.xi), 1]),
        ([request.k], [request.t ** 2, 0, 1]),
        ([request.k], [request.t ** 2, 2 * request.t, 1]),
    ]
    b5 = [request.k]
    a5 = [request.t ** 2, 2 * request.t * request.xi, 1]
    w5 = signal.TransferFunction(b5, a5)
    graphs = []
    for i, (b2_i, a2_i) in enumerate(b_n_a2):
        w2_i = signal.TransferFunction(b2_i, a2_i)
        graphs.append(MplCanvas(w5, a5, w2_i, a2_i))

    return "Построена область и график", graphs
