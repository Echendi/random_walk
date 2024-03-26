import numpy as np
from decimal import Decimal
from scipy.special import comb
from random_generator import CongruencialLineal

# Configuración de parámetros para el generador congruencial lineal
seed = 42  # Semilla inicial
k = 15686546789  # Constante k
c = 11  # Constante c
g = 30  # Constante g (Periodo 1073741823)
a = 1 + 2 * k  # Constante a
m = 2 ** g  # Módulo
next_step_generator = CongruencialLineal(a, c, m, seed)  # Generador para el próximo paso


def generate_moves(steps):
    """
        Genera una lista de números pseudoaleatorios utilizando el generador congruencial lineal.

        Args:
            steps (int): Número de pasos a generar.

        Returns:
            list: Lista de números pseudoaleatorios.
    """
    global seed, a, c, m
    generator = CongruencialLineal(a, c, m, seed)
    ri_values = [generator.generate_number() for _ in range(steps)]
    change_seed()
    return ri_values


def change_seed():
    """
        Cambia la semilla global aumentándola en 10.
    """
    global seed
    seed += 10


def generate_next_move():
    """
        Genera el próximo movimiento en la caminata aleatoria.

        Returns:
            float: Próximo movimiento generado.
    """
    global next_step_generator
    ri_value = next_step_generator.generate_number()
    return ri_value


def random_walk_1d(steps, source):
    """
        Realiza una caminata aleatoria 1D.

        Args:
            steps (int): Número de pasos en la caminata.
            source (int): Posición inicial.

        Returns:
            numpy.ndarray: Posiciones en la caminata aleatoria.
    """
    path = np.zeros(shape=steps + 1)
    path[0] = source
    step = source
    moves = generate_moves(steps)
    for i in range(0, steps):
        step = process_1d(moves[i], step)
        path[i + 1] = step
    return path


def go_to_1d(source, target_position):
    """
        Realiza una caminata aleatoria 1D desde una posición inicial hasta una posición objetivo.

        Args:
            source (int): Posición inicial.
            target_position (int): Posición objetivo.

        Returns:
            numpy.ndarray: Posiciones en la caminata aleatoria.
    """
    change_seed()
    step = source
    path = [source]
    while step != target_position:
        move = generate_next_move()
        step = process_1d(move, step)
        path.append(step)
    return np.array(path)


def process_1d(move, step):
    """
        Realiza un paso en la caminata aleatoria 1D.

        Args:
            move (float): Movimiento generado.
            step (int): Posición actual.

        Returns:
            int: Nueva posición después del paso.
    """
    if move > 0.5:
        step += 1
    else:
        step -= 1
    return step


# noinspection DuplicatedCode
def random_walk_2d(steps, source):
    """
        Realiza una caminata aleatoria 2D.

        Args:
            steps (int): Número de pasos en la caminata.
            source (tuple): Posición inicial en forma de tupla (x, y).

        Returns:
            numpy.ndarray: Posiciones en la caminata aleatoria en el eje x, y.
    """
    x_positions = np.zeros(shape=steps + 1)
    y_positions = np.zeros(shape=steps + 1)
    moves = generate_moves(steps)
    position = np.array(source)
    x_positions[0] = position[0]
    y_positions[0] = position[1]

    for i in range(0, steps):
        x_step, y_step = process_2d(moves[i])
        position = position + [x_step, y_step]
        x_positions[i + 1] = position[0]
        y_positions[i + 1] = position[1]

    return x_positions, y_positions


def process_2d(move):
    """
       Realiza un paso en la caminata aleatoria 2D.

       Args:
           move (float): Movimiento generado.

       Returns:
           tuple: Par de desplazamientos en los ejes x, y.
    """
    x_step = 0
    y_step = 0
    if move <= 0.25:
        x_step = 1
    elif 0.25 < move <= 0.5:
        x_step = -1
    elif 0.5 < move <= 0.75:
        y_step = 1
    else:
        y_step = -1
    return x_step, y_step


def go_to_2d(source, target_position):
    """
        Realiza una caminata aleatoria 2D desde una posición inicial hasta una posición objetivo.

        Args:
            source (tuple): Posición inicial en forma de tupla (x, y).
            target_position (tuple): Posición objetivo en forma de tupla (x, y).

        Returns:
            numpy.ndarray: Posiciones en la caminata aleatoria en el eje x, y.
    """
    change_seed()
    x_positions = [source[0]]
    y_positions = [source[1]]
    position = np.array(source)
    while position[0] != target_position[0] or position[1] != target_position[1]:
        move = generate_next_move()
        x_step, y_step = process_2d(move)
        position = position + [x_step, y_step]
        x_positions.append(position[0])
        y_positions.append(position[1])
    return np.array(x_positions), np.array(y_positions)


def random_walk_3d(steps, source):
    """
        Realiza una caminata aleatoria 3D.

        Args:
            steps (int): Número de pasos en la caminata.
            source (tuple): Posición inicial en forma de tupla (x, y, z).

        Returns:
            numpy.ndarray: Posiciones en la caminata aleatoria en los ejes x, y, z.
    """
    x_positions = np.zeros(shape=steps + 1)
    y_positions = np.zeros(shape=steps + 1)
    z_positions = np.zeros(shape=steps + 1)
    moves = generate_moves(steps)
    position = np.array(source)
    x_positions[0] = position[0]
    y_positions[0] = position[1]
    z_positions[0] = position[2]

    for i in range(0, steps):
        x_step, y_step, z_step = process_3d(moves[i])
        position = position + [x_step, y_step, z_step]
        x_positions[i + 1] = position[0]
        y_positions[i + 1] = position[1]
        z_positions[i + 1] = position[2]

    return x_positions, y_positions, z_positions


def process_3d(move):
    x_step = 0
    y_step = 0
    z_step = 0
    if move <= (1 / 6):
        x_step = 1
    elif (1 / 6) < move <= (2 / 6):
        x_step = -1
    elif (2 / 6) < move <= (3 / 6):
        y_step = 1
    elif (3 / 6) < move <= (4 / 6):
        y_step = -1
    elif (4 / 6) < move <= (5 / 6):
        z_step = 1
    else:
        z_step = -1
    return x_step, y_step, z_step


def go_to_3d(source, target_position):
    """
        Realiza una caminata aleatoria 3D desde una posición inicial hasta una posición objetivo.

        Args:
            source (tuple): Posición inicial en forma de tupla (x, y, z).
            target_position (tuple): Posición objetivo en forma de tupla (x, y, z).

        Returns:
            numpy.ndarray: Posiciones en la caminata aleatoria en los ejes x, y, z.
    """
    change_seed()
    x_positions = [source[0]]
    y_positions = [source[1]]
    z_positions = [source[2]]
    position = np.array(source)

    while position[0] != target_position[0] or position[1] != target_position[1] or position[2] != target_position[2]:
        move = generate_next_move()
        x_step, y_step, z_step = process_3d(move)
        position = position + [x_step, y_step, z_step]
        x_positions.append(position[0])
        y_positions.append(position[1])
        z_positions.append(position[2])
    return np.array(x_positions), np.array(y_positions), np.array(z_positions)


def calculate_1d_probability(steps, source, destination):
    """
        Calcula la probabilidad de una caminata aleatoria 1D desde una posición inicial hasta una posición objetivo.

        Args:
            steps (int): Número total de pasos en la caminata.
            source (int): Posición inicial.
            destination (int): Posición objetivo.

        Returns:
            Decimal: Probabilidad de alcanzar la posición objetivo.
    """
    distance = abs(destination - source)
    if (steps - distance) % 2 == 0:
        return Decimal(comb(steps, distance)) * (((Decimal(1) / Decimal(2)) ** Decimal(distance)) *
                                                 ((Decimal(1) / Decimal(2)) ** Decimal(steps - distance)))
    else:
        return 0


def calculate_2d_probability(steps, source, destination):
    """
        Calcula la probabilidad de una caminata aleatoria 2D desde una posición inicial hasta una posición objetivo.

        Args:
            steps (int): Número total de pasos en la caminata.
            source (tuple): Posición inicial en forma de tupla (x, y).
            destination (tuple): Posición objetivo en forma de tupla (x, y).

        Returns:
            Decimal: Probabilidad de alcanzar la posición objetivo.
    """
    distance = get_manhattan_distance(source, destination)
    if (steps - distance) % 2 == 0:
        return Decimal(comb(steps, distance)) * (((Decimal(1) / Decimal(4)) ** Decimal(distance)) *
                                                 ((Decimal(3) / Decimal(4)) ** Decimal(steps - distance)))
    else:
        return 0


def calculate_3d_probability(steps, source, destination):
    """
        Calcula la probabilidad de una caminata aleatoria 3D desde una posición inicial hasta una posición objetivo.

        Args:
            steps (int): Número total de pasos en la caminata.
            source (tuple): Posición inicial en forma de tupla (x, y, z).
            destination (tuple): Posición objetivo en forma de tupla (x, y, z).

        Returns:
            Decimal: Probabilidad de alcanzar la posición objetivo.
    """
    distance = get_manhattan_distance(source, destination)
    if (steps - distance) % 2 == 0:
        return Decimal(comb(steps, distance)) * (((Decimal(1) / Decimal(6)) ** Decimal(distance)) *
                                                 ((Decimal(5) / Decimal(6)) ** Decimal(steps - distance)))
    else:
        return 0


def get_manhattan_distance(point1, point2):
    """
        Calcula la distancia de Manhattan entre dos puntos en un espacio.

        Args:
            point1 (tuple): Coordenadas del primer punto en forma de tupla (x, y, z).
            point2 (tuple): Coordenadas del segundo punto en forma de tupla (x, y, z).

        Returns:
            int: Distancia de Manhattan entre los dos puntos.
        """
    return sum(abs(x_pos - y_pos) for x_pos, y_pos in zip(point1, point2))


if __name__ == '__main__':
    # print(calculate_1d_probability(1, 0, 1))
    # print("P([250,300])",calculate_2d_probability(550, [0, 0], [250, 300]))
    # print("P([45,23,17])",calculate_3d_probability(85, [0, 0, 0], [45, 23, 17]))
    # print(calculate_3d_probability(1, [0, 0, 0], [0, 0, 1]))
    x_s, y_s, z_s = go_to_3d((0, 0, 0), (0, 1, 0))
    for x, y, z in zip(x_s, y_s, z_s):
        print([x, y, z])
