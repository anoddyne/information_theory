import numpy as np

# вычисляем энтропию случайной переменной
def Enthropy(p):
    # добавляем небольшое значение к вероятностям, тк log(0) не определен
    p = p + 1e-10
    # вычисляем энтропию по формуле
    return -np.sum(p * np.log2(p))

# вычисляем совместную энтропию двух случайных переменных
def JointEntropy(p_xy):
    # делаем массив одномерным (плоским) и вычисляем энтропию
    return Enthropy(p_xy.flatten())

# вычисляем условную энтропию одной случайной переменной относительно другой
def ConditionalEnthropy(p_xy):
    H_XY = JointEntropy(p_xy)
    # вычисляем энтропию второй случайной переменной
    H_Y = Enthropy(np.sum(p_xy, axis=0))
    return H_XY - H_Y

# вычисляем взаимную информацию между двумя случайными переменными
def MutualInfo(p_xy):
    # вычисляем энтропию первой случайной переменной
    H_X = Enthropy(np.sum(p_xy, axis=1))
    # вычисляем энтропию второй случайной переменной
    H_Y = Enthropy(np.sum(p_xy, axis=0))
    # вычисляем совместную энтропию
    H_XY = JointEntropy(p_xy)
    return H_X + H_Y - H_XY

p_xy = np.loadtxt('input1.txt')
H_X = Enthropy(np.sum(p_xy, axis=1))
H_Y = Enthropy(np.sum(p_xy, axis=0))
H_XY = JointEntropy(p_xy)
H_X_Y = ConditionalEnthropy(p_xy)
H_Y_X = H_XY - H_X
I_XY = MutualInfo(p_xy)

print(f'H(X) = {H_X}\n'
      f'H(Y) = {H_Y}\n'
      f'H(X|Y) = {H_X_Y}\n'
      f'H(Y|X) = {H_Y_X}\n'
      f'H(X,Y) = {H_XY}\n'
      f'I(X;Y) = {I_XY}')
