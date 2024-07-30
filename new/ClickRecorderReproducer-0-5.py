import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
from pynput import mouse, keyboard
import threading
import time
import os

class ClickRecorderReproducer:
    def __init__(self, master):
        self.master = master
        self.master.title("Click Recorder and Reproducer")
        self.master.geometry("640x640")
        
        self.recording = False
        self.paused = False
        self.playing = False
        self.filepath = ""
        self.events = []

        self.load_images()
        self.create_widgets()

        self.mouse_listener = mouse.Listener(
            on_click=self.on_click,
            on_move=self.on_move)
        self.keyboard_listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release)

        self.mouse_listener.start()
        self.keyboard_listener.start()

    def load_images(self):
        # Carregar as imagens dos botões de movimento
        directions = ['up', 'down', 'left', 'right', 'up_left', 'up_right', 'down_left', 'down_right']
        self.images = {}
        for direction in directions:
            image = Image.open(f'/mnt/data/teclas-movimento-1.jpg')
            self.images[direction] = ImageTk.PhotoImage(image)

    def create_widgets(self):
        self.start_button = tk.Button(self.master, text="Iniciar Gravação", command=self.start_recording)
        self.start_button.pack()

        self.pause_button = tk.Button(self.master, text="Pausar Gravação", command=self.pause_recording)
        self.pause_button.pack()

        self.stop_button = tk.Button(self.master, text="Parar Gravação", command=self.stop_recording)
        self.stop_button.pack()

        self.choose_path_button = tk.Button(self.master, text="Escolher Caminho", command=self.choose_path)
        self.choose_path_button.pack()

        self.choose_file_button = tk.Button(self.master, text="Escolher Arquivo", command=self.choose_file)
        self.choose_file_button.pack()

        self.playback_button = tk.Button(self.master, text="Reproduzir", command=self.start_playback)
        self.playback_button.pack()

        self.exit_button = tk.Button(self.master, text="Sair", command=self.exit_application)
        self.exit_button.pack()

        self.status_label = tk.Label(self.master, text="Status: Pronto")
        self.status_label.pack()

        self.create_movement_buttons()

    def create_movement_buttons(self):
        directions = [
            ("up_left", 0, 0), ("up", 0, 1), ("up_right", 0, 2),
            ("left", 1, 0), ("right", 1, 2),
            ("down_left", 2, 0), ("down", 2, 1), ("down_right", 2, 2)
        ]

        self.movement_frame = tk.Frame(self.master)
        self.movement_frame.pack()

        for direction, row, column in directions:
            button = tk.Button(self.movement_frame, image=self.images[direction], command=lambda d=direction: self.move_cursor(d))
            button.grid(row=row, column=column)

    def move_cursor(self, direction):
        step = 20
        if direction == 'up':
            self.mouse_listener._mouse_controller.move(0, -step)
        elif direction == 'down':
            self.mouse_listener._mouse_controller.move(0, step)
        elif direction == 'left':
            self.mouse_listener._mouse_controller.move(-step, 0)
        elif direction == 'right':
            self.mouse_listener._mouse_controller.move(step, 0)
        elif direction == 'up_left':
            self.mouse_listener._mouse_controller.move(-step, -step)
        elif direction == 'up_right':
            self.mouse_listener._mouse_controller.move(step, -step)
        elif direction == 'down_left':
            self.mouse_listener._mouse_controller.move(-step, step)
        elif direction == 'down_right':
            self.mouse_listener._mouse_controller.move(step, step)

    def start_recording(self):
        self.recording = True
        self.paused = False
        self.events = []
        self.update_status("Gravação iniciada")

    def pause_recording(self):
        self.paused = not self.paused
        status = "Gravação pausada" if self.paused else "Gravação retomada"
        self.update_status(status)

    def stop_recording(self):
        self.recording = False
        self.paused = False
        self.save_recording()
        self.update_status("Gravação parada e salva")

    def choose_path(self):
        self.filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if self.filepath:
            self.update_status(f"Caminho selecionado: {self.filepath}")

    def choose_file(self):
        self.filepath = filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])
        if self.filepath:
            self.update_status(f"Arquivo selecionado: {self.filepath}")

    def save_recording(self):
        if self.filepath:
            with open(self.filepath, 'w') as file:
                for event in self.events:
                    file.write(f"{event}\n")
            self.update_status("Gravação salva")

    def start_playback(self):
        if self.filepath:
            self.playing = True
            self.update_status("Reprodução iniciada")
            playback_thread = threading.Thread(target=self.playback_events)
            playback_thread.start()

    def playback_events(self):
        with open(self.filepath, 'r') as file:
            events = file.readlines()

        for event in events:
            if not self.playing:
                break
            parts = event.strip().split()
            if parts[0] == "Movimento":
                x, y = int(parts[2]), int(parts[3])
                self.mouse_listener._mouse_controller.position = (x, y)
            elif parts[0] in ["Pressionado", "Liberado"]:
                button = self.get_mouse_button(parts[1])
                action = mouse.Button.left if parts[0] == "Pressionado" else mouse.Button.right
                self.mouse_listener._mouse_controller.click(button, action)
            elif parts[0] == "Tecla":
                key = self.get_key(parts[1])
                action = keyboard.Controller().press if parts[2] == "pressionada" else keyboard.Controller().release
                action(key)
            time.sleep(0.01)  # Pequena pausa entre eventos

        self.update_status("Reprodução concluída")

    def stop_playback(self):
        self.playing = False
        self.update_status("Reprodução parada")

    def exit_application(self):
        self.master.quit()

    def update_status(self, message):
        self.status_label.config(text=f"Status: {message}")
        # Printando o status no console também (para debug)
        print(message)

    def on_click(self, x, y, button, pressed):
        if self.recording and not self.paused:
            action = "Pressionado" if pressed else "Liberado"
            self.events.append(f"{action} {button.name} em {x} {y}")
            self.update_status(f"{action} {button.name} em {x} {y}")

    def on_move(self, x, y):
        if self.recording and not self.paused:
            self.events.append(f"Movimento em {x} {y}")
            self.update_status(f"Movimento em {x} {y}")

    def on_press(self, key):
        if self.recording and not self.paused:
            key_name = key.name if isinstance(key, keyboard.Key) else str(key)
            self.events.append(f"Tecla {key_name} pressionada")
            self.update_status(f"Tecla {key_name} pressionada")

    def on_release(self, key):
        if self.recording and not self.paused:
            key_name = key.name if isinstance(key, keyboard.Key) else str(key)
            self.events.append(f"Tecla {key_name} liberada")
            self.update_status(f"Tecla {key_name} liberada")

    def get_mouse_button(self, button_name):
        try:
            return mouse.Button[button_name.lower()]
        except KeyError:
            return mouse.Button.left  # Padrão para o botão esquerdo

    def get_key(self, key_name):
        try:
            return keyboard.Key[key_name]
        except KeyError:
            return key_name  # Caso contrário, retorna o nome original

if __name__ == "__main__":
    root = tk.Tk()
    app = ClickRecorderReproducer(root)
    root.mainloop()
