import tkinter as tk  # Importa el módulo tkinter y lo abrevia como tk
import time  # Importa el módulo time


class TimerApp:
    def __init__(self, master):
        # Constructor de la clase TimerApp, recibe un widget master como argumento
        self.start_time = 0  # Tiempo de inicio inicializado a 0
        self.master = master  # Widget principal de la aplicación
        self.master.title("Timer")  # Título de la ventana

        self.elapsed_time = 0  # Tiempo transcurrido inicializado a 0
        self.running = False  # Bandera para indicar si el temporizador está en marcha

        # Creación de una etiqueta para mostrar el tiempo transcurrido
        self.time_label = tk.Label(master, text="Tiempo transcurrido: 0.0 segundos")
        self.time_label.grid(row=2, column=5, columnspan=2, padx=10, pady=10)  # Ubicación de la etiqueta en la interfaz

    def start_stop_timer(self):
        # Método para iniciar o detener el temporizador
        if not self.running:
            # Si el temporizador no está en marcha
            self.running = True  # Se marca como en marcha
            self.start_time = time.time()  # Se guarda el tiempo de inicio actual
            self.update_time()  # Se llama al método para comenzar a actualizar el tiempo
        else:
            # Si el temporizador está en marcha
            self.running = False  # Se marca como detenido

    def update_time(self):
        # Método para actualizar el tiempo transcurrido
        if self.running:
            # Si el temporizador está en marcha
            current_time = time.time()  # Se obtiene el tiempo actual
            self.elapsed_time = current_time - self.start_time  # Se calcula el tiempo transcurrido
            # Se actualiza la etiqueta con el tiempo transcurrido
            self.time_label.config(text="Tiempo transcurrido: {:.2f} segundos".format(self.elapsed_time))
            # Se programa una llamada recursiva para actualizar el tiempo cada 200 milisegundos
            self.master.after(200, self.update_time)

    def reset_timer(self):
        # Método para reiniciar el temporizador
        self.elapsed_time = 0  # Se reinicia el tiempo transcurrido
        # Se actualiza la etiqueta para mostrar "Tiempo transcurrido: 0.0 segundos"
        self.time_label.config(text="Tiempo transcurrido: 0.0 segundos")
        self.running = False  # Se marca el temporizador como detenido
