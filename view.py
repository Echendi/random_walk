import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import plotly.graph_objects as go
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import random_walk
from timer import TimerApp
import threading

# Inicialización de variables globales
running_threads = []  # Lista para almacenar hilos en ejecución
stop_event = threading.Event()  # Evento para detener todos los hilos

path_1d = []  # Almacenar la caminata aleatoria 1D
xs, ys, zs = [], [], []  # Almacenar las posiciones para caminatas 2D y 3D


# Función para detener todos los hilos en ejecución
def stop_all_threads():
    global running_threads
    reset_timer()  # Reiniciar el temporizador
    stop_event.set()  # Establecer el evento de parada


# Funciones para iniciar, detener y reiniciar un temporizador (presumiblemente definidas en otro lugar)
def start_stop_timer():
    timer_app.start_stop_timer()  # Llamar al método start_stop_timer de TimerApp


def update_time():
    timer_app.update_time()  # Llamar al método update_time de TimerApp


def reset_timer():
    timer_app.reset_timer()  # Llamar al método reset_timer de TimerApp


# Función para trazar la caminata aleatoria 1D
def plot_1d(path):
    plt.figure(1)
    plt.plot(path)
    plt.xlabel('Paso')
    plt.ylabel('Posición')
    plt.title('Trayectoria de la rana')

    canvas1 = FigureCanvasTkAgg(plt.gcf(), master=root)
    canvas1.draw()
    canvas1.get_tk_widget().grid(row=4, column=0, padx=10, pady=10, columnspan=3)


# Función para trazar la caminata aleatoria 2D

def plot_2d(x, y):
    fig, ax = plt.subplots(figsize=(5, 5))
    ax.plot(x, y)
    plt.title('Trayectoria de la rana')

    ax.axhline(0, color='black', linestyle='--', linewidth=0.5)  # Línea horizontal en y=0
    ax.axvline(0, color='black', linestyle='--', linewidth=0.5)  # Línea vertical en x=0
    ax.plot(x[-1], y[-1], 'ro')  # 'ro' para un punto rojo
    ax.annotate(f'({x[-1]}, {y[-1]})', (x[-1], y[-1]), textcoords="offset points", xytext=(-10, 10), ha='center')

    canvas1 = FigureCanvasTkAgg(plt.gcf(), master=root)
    canvas1.draw()
    canvas1.get_tk_widget().grid(row=4, column=0, padx=10, pady=10, columnspan=7)


# Función para trazar la caminata aleatoria 3D
def plot_3d(x, y, z):
    time = np.array(range(0, len(x)))
    fig = go.Figure(data=go.Scatter3d(
        x=x, y=y, z=z,
        marker=dict(
            size=4,
            color=time,
            colorscale='Plasma'
        ),
        line=dict(
            color='darkblue',
            width=2
        )
    ))
    fig.update_layout(margin=dict(l=0, r=0, b=0, t=0))

    fig.show()


# Función para trazar la frecuencia de valores en una caminata aleatoria
def plot_frequency(path):
    unique_values, counts = np.unique(path, return_counts=True)
    plt.figure(2)
    plt.bar(unique_values, counts)
    plt.xlabel('Valor')
    plt.ylabel('Frecuencia')
    plt.title('Frecuencias de los valores en el arreglo')

    canvas2 = FigureCanvasTkAgg(plt.gcf(), master=root)
    canvas2.draw()
    canvas2.get_tk_widget().grid(row=4, column=4, padx=10, pady=10, columnspan=3)


# Función para reiniciar las gráficas
def restart_plots():
    stop_all_threads()  # Detener todos los hilos
    label_total_steps.config(text=f"Se alcanzó el objetivo en 0 pasos")
    plt.close('all')  # Cerrar todas las gráficas
    for widget in root.grid_slaves(row=4):  # Encuentra los widgets en la fila 4 (donde se encuentran las gráficas)
        widget.grid_forget()  # Olvida los widgets de la cuadrícula


# Función para calcular la caminata aleatoria según la dimensión seleccionada
def calculate(dim):
    global stop_event
    stop_event.clear()  # Limpiar el evento de detención
    reset_timer()  # Reiniciar el temporizador
    label_total_steps.config(text=f"Se alcanzó el objetivo en 0 pasos")  # Actualizar la etiqueta de pasos

    try:
        steps = int(entry_steps.get())  # Obtener el número de pasos
        x_position = int(entry_x_position.get())  # Obtener la posición x
        y_position = 0
        z_position = 0

        if dim >= 1:
            y_position = int(entry_y_position.get())  # Obtener la posición y
        if dim == 2:
            z_position = int(entry_z_position.get())  # Obtener la posición z

        start_stop_timer()  # Iniciar el temporizador

        option = option_var.get()  # Obtener la opción seleccionada (Pasos u Objetivo)
        if option == "Pasos":
            if dim == 0:
                thread = threading.Thread(target=generate_random_walk_1d, args=(steps, x_position))
                thread.start()
                running_threads.append(thread)
            elif dim == 1:
                thread = threading.Thread(target=generate_random_walk_2d, args=(steps, x_position, y_position))
                thread.start()
                running_threads.append(thread)
            else:
                thread = threading.Thread(target=generate_random_walk_3d,
                                          args=(steps, x_position, y_position, z_position))
                thread.start()
                running_threads.append(thread)
        else:
            if dim == 0:
                thread = threading.Thread(target=generate_random_target_1d, args=(x_position,))
                thread.start()
                running_threads.append(thread)
                probability = random_walk.calculate_1d_probability(abs(x_position), 0, x_position)
                label_probability.config(text=f"La probabilidad de llegar a la posición {x_position} en "
                                              f"{abs(x_position)} pasos es {probability}")
            elif dim == 1:
                thread = threading.Thread(target=generate_random_target_2d, args=(x_position, y_position))
                thread.start()
                running_threads.append(thread)
                min_steps = random_walk.get_manhattan_distance((0, 0), (x_position, y_position))
                probability = random_walk.calculate_2d_probability(min_steps, (0, 0), (x_position, y_position))
                label_probability.config(
                    text=f"La probabilidad de llegar a la posición ( {x_position}, {y_position} ) en {min_steps} "
                         f"pasos es {probability}")
            else:
                thread = threading.Thread(target=generate_random_target_3d, args=(x_position, y_position, z_position))
                thread.start()
                running_threads.append(thread)
                min_steps = random_walk.get_manhattan_distance((0, 0, 0), (x_position, y_position, z_position))
                probability = random_walk.calculate_3d_probability(min_steps, (0, 0, 0), (x_position,
                                                                                          y_position, z_position))
                label_probability.config(
                    text=f"La probabilidad de llegar a la posición ( {x_position}, {y_position}, {z_position} ) en "
                         f"{min_steps} pasos es {probability}")

    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")


# Funciones para generar la caminata aleatoria y el objetivo de manera asíncrona
def generate_random_walk_1d(steps, x_position):
    global path_1d
    path_1d = random_walk.random_walk_1d(steps, x_position)
    root.event_generate("<<RandomWalkGenerated>>")


def generate_random_target_1d(x_target):
    global path_1d
    path_1d = random_walk.go_to_1d(0, x_target)
    root.event_generate("<<RandomWalkGenerated>>")
    label_total_steps.config(text=f"Se alcanzó el objetivo en {len(path_1d) - 1} pasos")


def generate_random_walk_2d(steps, x_position, y_position):
    global xs, ys
    xs, ys = random_walk.random_walk_2d(steps, (x_position, y_position))
    root.event_generate("<<2DRandomWalkGenerated>>")


def generate_random_target_2d(x_target, y_target):
    global xs, ys
    xs, ys = random_walk.go_to_2d((0, 0), (x_target, y_target))
    root.event_generate("<<2DRandomWalkGenerated>>")
    label_total_steps.config(text=f"Se alcanzó el objetivo en {len(xs) - 1} pasos")


def generate_random_walk_3d(steps, x_position, y_position, z_position):
    global xs, ys, zs
    xs, ys, zs = random_walk.random_walk_3d(steps, (x_position, y_position, z_position))
    root.event_generate("<<3DRandomWalkGenerated>>")


def generate_random_target_3d(x_target, y_target, z_target):
    global xs, ys, zs
    xs, ys, zs = random_walk.go_to_3d((0, 0, 0), (x_target, y_target, z_target))
    root.event_generate("<<3DRandomWalkGenerated>>")
    label_total_steps.config(text=f"Se alcanzó el objetivo en {len(xs) - 1} pasos")


# Manejadores de eventos para trazar las caminatas aleatorias después de ser generadas
def on_random_walk_generated(event):
    start_stop_timer()
    plot_1d(path_1d)
    plot_frequency(path_1d)


def on_2d_random_walk_generated(event):
    global xs, ys
    start_stop_timer()
    plot_2d(xs, ys)


def on_3d_random_walk_generated(event):
    global xs, ys, zs
    start_stop_timer()
    plot_3d(xs, ys, zs)


# Manejadores de eventos para actualizar la interfaz cuando se selecciona una dimensión u opción
def dimension_selected(event):
    selected_dim = dimension_var.get()

    if selected_dim == "1D":
        entry_y_position.config(state='disabled')
        entry_z_position.config(state='disabled')
    elif selected_dim == "2D":
        entry_y_position.config(state='normal')
        entry_z_position.config(state='disabled')
    else:
        entry_y_position.config(state='normal')
        entry_z_position.config(state='normal')

    entry_x_position.delete(0, tk.END)
    entry_x_position.insert(0, "0")
    entry_y_position.delete(0, tk.END)
    entry_y_position.insert(0, "0")
    entry_z_position.delete(0, tk.END)
    entry_z_position.insert(0, "0")
    restart_plots()


def option_selected(event):
    option = option_var.get()
    restart_plots()
    if option == "Pasos":
        label_target.config(text="Origen")
        entry_steps.config(state='normal')
        for widget in root.grid_slaves(row=3):  # Encuentra los widgets en la fila 3
            widget.grid_forget()  # Olvida los widgets de la cuadrícula
    else:
        label_target.config(text="Objetivo")
        entry_steps.config(state='disabled')
        label_probability.grid(row=3, column=0, columnspan=3, padx=10, pady=5)
        label_total_steps.grid(row=3, column=3, columnspan=3, padx=10, pady=5)
        label_probability.config(text="Probabilidad:")
        label_total_steps.config(text=f"Se alcanzó el objetivo en 0 pasos")


# Crea la ventana principal
root = tk.Tk()
root.title("Caminatas aleatorias")
timer_app = TimerApp(root)

# Crear el menú desplegable para seleccionar la dimensión
dimension_var = tk.StringVar(root)
dimension_var.set("1D")
dimension_menu = tk.OptionMenu(root, dimension_var, "1D", "2D", "3D", command=dimension_selected)
dimension_menu.grid(row=0, column=0, columnspan=1, padx=10, pady=5)

# Crear el menú desplegable para seleccionar la opción
option_var = tk.StringVar(root)
option_var.set("Pasos")
option_menu = tk.OptionMenu(root, option_var, "Pasos", "Posición Objetivo", command=option_selected)
option_menu.grid(row=0, column=1, columnspan=3, padx=10, pady=5)

# Crear los widgets para los campos de entrada
label_steps = tk.Label(root, text="Cantidad de Pasos:")
label_steps.grid(row=0, column=4, padx=10, pady=5)
entry_steps = tk.Entry(root, width=10)
entry_steps.insert(tk.END, "1000")
entry_steps.grid(row=0, column=5, padx=10, pady=5)

label_target = tk.Label(root, width=10, text="Origen")
label_target.grid(row=1, column=0, padx=10, pady=5)
label_target_x = tk.Label(root, width=5, text="x:")
label_target_x.grid(row=1, column=1, padx=10, pady=5)
entry_x_position = tk.Entry(root, width=7)
entry_x_position.insert(tk.END, "0")
entry_x_position.grid(row=1, column=2, padx=10, pady=5)

label_target_y = tk.Label(root, width=5, text="y:")
label_target_y.grid(row=1, column=3, padx=10, pady=5)
entry_y_position = tk.Entry(root, state='disabled', width=7)
entry_y_position.grid(row=1, column=4, padx=10, pady=5)

label_target_z = tk.Label(root, width=5, text="z:")
label_target_z.grid(row=1, column=5, padx=10, pady=5)
entry_z_position = tk.Entry(root, state='disabled', width=7)
entry_z_position.grid(row=1, column=6, padx=10, pady=5)

button_calculate = tk.Button(root, text="Calcular",
                             command=lambda: calculate(["1D", "2D", "3D"].index(dimension_var.get())))
button_calculate.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

button_restart_plots = tk.Button(root, text="Reiniciar Gráficas", command=restart_plots)
button_restart_plots.grid(row=2, column=3, columnspan=2, padx=10, pady=5)

label_probability = tk.Label(root, text="Probabilidad:")
label_total_steps = tk.Label(root, text=f"Se alcanzó el objetivo en 0 pasos")

# Ejecuta el bucle principal de la aplicación
root.bind("<<RandomWalkGenerated>>", on_random_walk_generated)
root.bind("<<2DRandomWalkGenerated>>", on_2d_random_walk_generated)
root.bind("<<3DRandomWalkGenerated>>", on_3d_random_walk_generated)
root.mainloop()
