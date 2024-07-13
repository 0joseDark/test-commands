# pip install pynput

import tkinter as tk
from tkinter import filedialog, messagebox
from pynput import mouse, keyboard
import threading
import time

class ClickRecorder:
    def __init__(self, root):
        self.root = root
        self.root.title("Gravador de Cliques")
        self.root.geometry("640x640")

        # Estado inicial das variáveis
        self.recording = False
        self.paused = False
        self.filepath = ""
        self.events = []

        # Criação dos botões
        self.create_widgets()

        # Listeners de mouse e teclado
        self.mouse_listener = mouse.Listener(on_click=self.on_click)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)

    def create_widgets(self):
        # Botão Ligar
        self.start_button = tk.Button(self.root, text="Ligar", command=self.start_recording)
        self.start_button.pack(pady=10)

        # Botão Pausa
        self.pause_button = tk.Button(self.root, text="Pausa", command=self.pause_recording)
        self.pause_button.pack(pady=10)

        # Botão Gravar
        self.record_button = tk.Button(self.root, text="Gravar", command=self.save_recording)
        self.record_button.pack(pady=10)

        # Botão Sair
        self.quit_button = tk.Button(self.root, text="Sair", command=self.root.quit)
        self.quit_button.pack(pady=10)

        # Botão Escolher Caminho do Arquivo
        self.choose_path_button = tk.Button(self.root, text="Escolher Caminho", command=self.choose_path)
        self.choose_path_button.pack(pady=10)

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.paused = False
            self.events.clear()  # Limpa eventos anteriores
            self.mouse_listener.start()
            self.keyboard_listener.start()
            self.update_status("Gravação iniciada")

    def pause_recording(self):
        if self.recording:
            self.paused = not self.paused
            status = "Pausado" if self.paused else "Retomado"
            self.update_status(status)

    def save_recording(self):
        if self.filepath:
            with open(self.filepath, 'w') as f:
                for event in self.events:
                    f.write(f"{event}\n")
            self.update_status("Gravação salva")
        else:
            messagebox.showwarning("Aviso", "Escolha um caminho para salvar o arquivo")

    def choose_path(self):
        self.filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if self.filepath:
            self.update_status(f"Caminho selecionado: {self.filepath}")

    def update_status(self, message):
        print(message)

    def on_click(self, x, y, button, pressed):
        if self.recording and not self.paused:
            self.events.append(f"{'Pressionado' if pressed else 'Liberado'} botão {button} em ({x}, {y})")

    def on_press(self, key):
        if self.recording and not self.paused:
            self.events.append(f"Tecla {key} pressionada")

    def on_release(self, key):
        if self.recording and not self.paused:
            self.events.append(f"Tecla {key} liberada")

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    root = tk.Tk()
    app = ClickRecorder(root)
    app.run()
