# pip install pynput

import tkinter as tk
from tkinter import filedialog, messagebox
from pynput import mouse, keyboard
import threading
import time

class ClickRecorderReproducer:
    def __init__(self, root):
        self.root = root
        self.root.title("Gravador e Reprodutor de Cliques")
        self.root.geometry("640x640")

        # Estado inicial das variáveis
        self.recording = False
        self.filepath = ""
        self.events = []

        # Criação dos botões
        self.create_widgets()

        # Listeners de mouse e teclado
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        
        self.playback_thread = None

    def create_widgets(self):
        # Botão Ligar
        self.start_button = tk.Button(self.root, text="Ligar", command=self.start_recording)
        self.start_button.pack(pady=10)

        # Botão Escolher Caminho do Arquivo
        self.choose_path_button = tk.Button(self.root, text="Escolher Caminho para Gravação", command=self.choose_path)
        self.choose_path_button.pack(pady=10)

        # Botão Escolher Arquivo para Reprodução
        self.choose_file_button = tk.Button(self.root, text="Escolher Arquivo para Reprodução", command=self.choose_file)
        self.choose_file_button.pack(pady=10)

        # Botão Reproduzir
        self.play_button = tk.Button(self.root, text="Reproduzir", command=self.start_playback)
        self.play_button.pack(pady=10)

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.events.clear()  # Limpa eventos anteriores
            self.mouse_listener.start()
            self.keyboard_listener.start()
            self.update_status("Gravação iniciada")

    def choose_path(self):
        self.filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if self.filepath:
            self.update_status(f"Caminho selecionado: {self.filepath}")

    def choose_file(self):
        self.filepath = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if self.filepath:
            self.update_status(f"Arquivo selecionado: {self.filepath}")

    def save_recording(self):
        if self.filepath:
            with open(self.filepath, 'w') as f:
                for event in self.events:
                    f.write(f"{event}\n")
            self.update_status("Gravação salva")
        else:
            messagebox.showwarning("Aviso", "Escolha um caminho para salvar o arquivo")

    def start_playback(self):
        if self.filepath:
            self.playback_thread = threading.Thread(target=self.playback_events)
            self.playback_thread.start()
        else:
            messagebox.showwarning("Aviso", "Escolha um arquivo para reprodução")

    def playback_events(self):
        with open(self.filepath, 'r') as f:
            lines = f.readlines()

        mouse_controller = mouse.Controller()
        keyboard_controller = keyboard.Controller()

        for line in lines:
            parts = line.strip().split()
            event_type = parts[0]
            if event_type == "Pressionado":
                button = mouse.Button[parts[2].lower()]
                x, y = int(parts[4][1:]), int(parts[5][:-1])
                mouse_controller.position = (x, y)
                mouse_controller.press(button)
            elif event_type == "Liberado":
                button = mouse.Button[parts[2].lower()]
                x, y = int(parts[4][1:]), int(parts[5][:-1])
                mouse_controller.position = (x, y)
                mouse_controller.release(button)
            elif event_type == "Tecla":
                key_action = parts[2]
                key = keyboard.Key[parts[1][4:]] if parts[1].startswith("Key.") else parts[1]
                if key_action == "pressionada":
                    keyboard_controller.press(key)
                elif key_action == "liberada":
                    keyboard_controller.release(key)
            time.sleep(0.01)  # Pequeno atraso para simular o tempo entre os eventos

    def update_status(self, message):
        print(message)

    def on_click(self, x, y, button, pressed):
        if self.recording:
            self.events.append(f"{'Pressionado' if pressed else 'Liberado'} botão {button} em ({x}, {y})")

    def on_press(self, key):
        if self.recording:
            self.events.append(f"Tecla {key} pressionada")

    def on_release(self, key):
        if self.recording:
            self.events.append(f"Tecla {key} liberada")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClickRecorderReproducer(root)
    app.run()
