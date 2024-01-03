import numpy as np
import matplotlib.pyplot as plt
from scipy import signal

# это условия по вариантам, конкретно тут 1й
#k = 0.5 #коэф усиления
#T = 2 # постоянная времени
#xi = 0.6
k = 1 #коэф усиления
T = 1 # постоянная времени
xi = 0.2
def draw_shit(W, A):
    # Step Response
    plt.subplot(3, 2, 1)
    t, y = signal.step(W)
    plt.plot(t, y)
    plt.xlabel('Time')
    plt.ylabel('Step Response')
    plt.title('Step Response')
    plt.grid(True)

    # Impulse Response
    plt.subplot(3, 2, 2)
    t, y = signal.impulse(W)
    plt.plot(t, y)
    plt.xlabel('Time')
    plt.ylabel('Impulse Response')
    plt.title('Impulse Response')
    plt.grid(True)

    # Bode Plot - Magnitude
    plt.subplot(3, 2, 3)
    w, mag, phase = signal.bode(W)
    plt.semilogx(w, mag)
    plt.xlabel('Frequency')
    plt.ylabel('Magnitude (dB)')
    plt.title('Bode Plot - Magnitude')
    plt.grid(True)

    # Bode Plot - Phase
    plt.subplot(3, 2, 4)
    plt.semilogx(w, phase)
    plt.xlabel('Frequency')
    plt.ylabel('Phase (degrees)')
    plt.title('Bode Plot - Phase')
    plt.grid(True)

    # Nyquist Plot
    plt.subplot(3, 2, 5)
    w, h = signal.freqresp(W)
    plt.plot(h.real, h.imag)
    plt.xlabel('Real')
    plt.ylabel('Imaginary')
    plt.title('Nyquist Plot')
    plt.grid(True)

    # Pole-Zero Map
    plt.subplot(3, 2, 6)
    poles = np.roots(A)
    plt.plot(poles.real, poles.imag, 'x')
    plt.xlabel('Real')
    plt.ylabel('Imaginary')
    plt.title('Pole-Zero Map')
    plt.grid(True)

    plt.tight_layout()  # Улучшает распределение графиков на изображении
    plt.show()

def draw_2_shit(W, A, W2, A2):

    # Step Response
    plt.subplot(3, 2, 1)
    t, y = signal.step(W)
    plt.plot(t, y, label='W', color='blue')  # Указываем цвет синий для W
    t, y = signal.step(W2)
    plt.plot(t, y, label='W2', color='red')  # Указываем цвет красный для W2
    plt.xlabel('Time')
    plt.ylabel('Step Response')
    plt.title('Step Response')
    plt.grid(True)
    plt.legend()

    # Impulse Response
    plt.subplot(3, 2, 2)
    t, y = signal.impulse(W)
    plt.plot(t, y, label='W', color='blue')
    t, y = signal.impulse(W2)
    plt.plot(t, y, label='W2', color='red')
    plt.xlabel('Time')
    plt.ylabel('Impulse Response')
    plt.title('Impulse Response')
    plt.grid(True)
    plt.legend()

    # Bode Plot - Magnitude
    plt.subplot(3, 2, 3)
    w, mag, phase = signal.bode(W)
    plt.semilogx(w, mag, label='W', color='blue')
    w, mag, phase = signal.bode(W2)
    plt.semilogx(w, mag, label='W2', color='red')
    plt.xlabel('Frequency')
    plt.ylabel('Magnitude (dB)')
    plt.title('Bode Plot - Magnitude')
    plt.grid(True)
    plt.legend()

    # Bode Plot - Phase
    plt.subplot(3, 2, 4)
    #w, phase = signal.bode(W)
    plt.semilogx(w, phase, label='W', color='blue')
    #w, phase = signal.bode(W2)
    plt.semilogx(w, phase, label='W2', color='red')
    plt.xlabel('Frequency')
    plt.ylabel('Phase (degrees)')
    plt.title('Bode Plot - Phase')
    plt.grid(True)
    plt.legend()

    # Nyquist Plot
    plt.subplot(3, 2, 5)
    w, h = signal.freqresp(W)
    plt.plot(h.real, h.imag, label='W', color='blue')
    w, h = signal.freqresp(W2)
    plt.plot(h.real, h.imag, label='W2', color='red')
    plt.xlabel('Real')
    plt.ylabel('Imaginary')
    plt.title('Nyquist Plot')
    plt.grid(True)
    plt.legend()

    # Pole-Zero Map
    plt.subplot(3, 2, 6)
    poles = np.roots(A)
    plt.plot(poles.real, poles.imag, 'x', label='W', color='blue')
    poles = np.roots(A2)
    plt.plot(poles.real, poles.imag, 'x', label='W2', color='red')
    plt.xlabel('Real')
    plt.ylabel('Imaginary')
    plt.title('Pole-Zero Map')
    plt.grid(True)
    plt.legend()

    plt.tight_layout()  # Улучшает распределение графиков на изображении
    plt.show()


b_n_a=[([k], [0, 0, 1]),           #OK
       ([k], [0, 1, 0]),           #OK
       ([k], [0, T, 1]),           #OK
       ([k, 0], [0, T, 1]),        #OK
       ([k], [T**2, 2*T*xi, 1]),   #OK
       ]
b_n_a2 = [
       ([2*k], [T**2, 2*T*xi, 1]),
       ([k], [(2*T)**2, 2*2*T*xi, 1]),
       ([k], [T**2, 2*T*(0.5*xi), 1]),
       ([k], [T**2, 0, 1]),
       ([k], [T**2, 2*T, 1]),
]



#B5 = [k]
#A5 = [T**2, 2*T*xi, 1]
#W = signal.TransferFunction(B5, A5)

for i, (B_i, A_i) in enumerate(b_n_a):
    print(i+1)
    W_i = signal.TransferFunction(B_i, A_i)
    draw_shit(W_i, A_i)

B5 = [k]
A5 = [T**2, 2*T*xi, 1]
W5 = signal.TransferFunction(B5, A5)
for i, (B2_i, A2_i) in enumerate(b_n_a2):
    print(i+6)
    W2_i = signal.TransferFunction(B2_i, A2_i)
    draw_2_shit(W=W5, A=A5, W2=W2_i, A2=A2_i)
