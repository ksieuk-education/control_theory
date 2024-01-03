import numpy as np
from scipy import signal
import matplotlib.backends.backend_qtagg as matplotlib_backend_qtagg
import matplotlib.figure as matplotlib_figure
import lib.methods.first_lab.models as methods_first_lab_models


class MplCanvas(matplotlib_backend_qtagg.FigureCanvasQTAgg):
    def __init__(
            self, w, a, width=8, height=6, dpi=100,
    ):
        self.w = w
        self.a = a
        plt_ = matplotlib_figure.Figure(figsize=(width, height), dpi=dpi)
        plt_.tight_layout()
        plt_.subplots_adjust(hspace=0.5, wspace=0.3)

        self.axes = plt_.add_subplot(321)
        t, y = signal.step(w)
        self.axes.plot(t, y)
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('Step Response')
        self.axes.set_title('Step Response')
        self.axes.grid(True)

        # Impulse Response
        self.axes = plt_.add_subplot(3, 2, 2)
        t, y = signal.impulse(w)
        self.axes.plot(t, y)
        self.axes.set_xlabel('Time')
        self.axes.set_ylabel('Impulse Response')
        self.axes.set_title('Impulse Response')
        self.axes.grid(True)

        # Bode Plot - Magnitude
        self.axes = plt_.add_subplot(3, 2, 3)
        w_, mag, phase = signal.bode(w)
        self.axes.semilogx(w_, mag)
        self.axes.set_xlabel('Frequency')
        self.axes.set_ylabel('Magnitude (dB)')
        self.axes.set_title('Bode Plot - Magnitude')
        self.axes.grid(True)

        # Bode Plot - Phase
        self.axes = plt_.add_subplot(3, 2, 4)
        self.axes.semilogx(w_, phase)
        self.axes.set_xlabel('Frequency')
        self.axes.set_ylabel('Phase (degrees)')
        self.axes.set_title('Bode Plot - Phase')
        self.axes.grid(True)

        # Nyquist Plot
        self.axes = plt_.add_subplot(3, 2, 5)
        w_, h = signal.freqresp(w)
        self.axes.plot(h.real, h.imag)
        self.axes.set_xlabel('Real')
        self.axes.set_ylabel('Imaginary')
        self.axes.set_title('Nyquist Plot')
        self.axes.grid(True)

        # Pole-Zero Map
        self.axes = plt_.add_subplot(3, 2, 6)
        poles = np.roots(a)
        self.axes.plot(poles.real, poles.imag, 'x')
        self.axes.set_xlabel('Real')
        self.axes.set_ylabel('Imaginary')
        self.axes.set_title('Pole-Zero Map')
        self.axes.grid(True)

        super(MplCanvas, self).__init__(plt_)

    def get_copy(self):
        return MplCanvas(self.w, self.a)


def calculate_method(request: methods_first_lab_models.FirstLabModel):
    b_n_a = [([request.k], [0, 0, 1]),  # OK
             ([request.k], [0, 1, 0]),  # OK
             ([request.k], [0, request.t, 1]),  # OK
             ([request.k, 0], [0, request.t, 1]),  # OK
             ([request.k], [request.t ** 2, 2 * request.t * request.xi, 1]),  # OK
             ]

    graphs = []
    for i, (b_i, a_i) in enumerate(b_n_a):
        w_i = signal.TransferFunction(b_i, a_i)
        graphs.append(MplCanvas(w_i, a_i))

    return "Построена область и график", graphs
