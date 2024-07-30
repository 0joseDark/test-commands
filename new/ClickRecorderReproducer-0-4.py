import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
from pynput import mouse, keyboard
import threading
import time
import os

class ClickRecorderReproducer:
    def __init__(self, root):
        # Inicializa a janela principal
        self.root = root
        self.root.title("Gravador e Reprodutor de Cliques")
        self.root.geometry("640x640")

        # Estado inicial das variáveis
        self.recording = False
        self.paused = False
        self.playing = False
        self.filepath = ""
        self.events = []

        # Carregar imagens dos botões de movimento
        self.load_images()

        # Criação dos botões
        self.create_widgets()

        # Listeners de mouse e teclado
        self.mouse_listener = mouse.Listener(on_click=self.on_click, on_move=self.on_move)
        self.keyboard_listener = keyboard.Listener(on_press=self.on_press, on_release=self.on_release)
        
        self.playback_thread = None

    def load_images(self):
        # Carregar as imagens dos botões
        self.images = {}
        directions = ['up', 'down', 'left', 'right', 'up_left', 'up_right', 'down_left', 'down_right']
        for direction in directions:
            image_path = os.path.join(os.path.dirname(__file__), f'teclas-movimento-{direction}.jpg')
            if os.path.exists(image_path):
                image = Image.open(image_path)
                self.images[direction] = ImageTk.PhotoImage(image)
            else:
                print(f"Imagem {image_path} não encontrada")

    def create_widgets(self):
        # Cria o botão Ligar
        self.start_button = tk.Button(self.root, text="Ligar", command=self.start_recording)
        self.start_button.pack(pady=10)

        # Cria o botão Pausa
        self.pause_button = tk.Button(self.root, text="Pausa", command=self.pause_recording)
        self.pause_button.pack(pady=10)

        # Cria o botão Parar
        self.stop_button = tk.Button(self.root, text="Parar", command=self.stop_recording)
        self.stop_button.pack(pady=10)

        # Cria o botão Escolher Caminho do Arquivo
        self.choose_path_button = tk.Button(self.root, text="Escolher Caminho para Gravação", command=self.choose_path)
        self.choose_path_button.pack(pady=10)

        # Cria o botão Escolher Arquivo para Reprodução
        self.choose_file_button = tk.Button(self.root, text="Escolher Arquivo para Reprodução", command=self.choose_file)
        self.choose_file_button.pack(pady=10)

        # Cria o botão Reproduzir
        self.play_button = tk.Button(self.root, text="Reproduzir", command=self.start_playback)
        self.play_button.pack(pady=10)

        # Cria o botão Sair
        self.exit_button = tk.Button(self.root, text="Sair", command=self.exit_application)
        self.exit_button.pack(pady=10)

        # Cria os botões de movimento do mouse
        self.create_movement_buttons()

    def create_movement_buttons(self):
        # Cria botões de movimento do mouse usando as imagens carregadas
        movement_frame = tk.Frame(self.root)
        movement_frame.pack(pady=20)

        directions = [
            ('up_left', 0, 0), ('up', 0, 1), ('up_right', 0, 2),
            ('left', 1, 0), ('right', 1, 2),
            ('down_left', 2, 0), ('down', 2, 1), ('down_right', 2, 2)
        ]
        functions = {
            'up': self.move_up, 'down': self.move_down, 'left': self.move_left, 'right': self.move_right, 
            'up_left': self.move_up_left, 'up_right': self.move_up_right, 'down_left': self.move_down_left, 'down_right': self.move_down_right
        }

        for direction, row, col in directions:
            if direction in self.images:
                button = tk.Button(movement_frame, image=self.images[direction], command=functions[direction])
                button.grid(row=row, column=col, padx=5, pady=5)

    def move_up(self):
        mouse.Controller().move(0, -10)

    def move_down(self):
        mouse.Controller().move(0, 10)

    def move_left(self):
        mouse.Controller().move(-10, 0)

    def move_right(self):
        mouse.Controller().move(10, 0)

    def move_up_left(self):
        mouse.Controller().move(-10, -10)

    def move_up_right(self):
        mouse.Controller().move(10, -10)

    def move_down_left(self):
        mouse.Controller().move(-10, 10)

    def move_down_right(self):
        mouse.Controller().move(10, 10)

    def start_recording(self):
        # Inicia a gravação de eventos
        if not self.recording:
            self.recording = True
            self.paused = False
            self.events.clear()  # Limpa eventos anteriores
            self.mouse_listener.start()
            self.keyboard_listener.start()
            self.update_status("Gravação iniciada")

    def pause_recording(self):
        # Pausa ou retoma a gravação
        if self.recording:
            self.paused = not self.paused
            status = "Pausado" if self.paused else "Retomado"
            self.update_status(status)

    def stop_recording(self):
        # Para a gravação e salva os eventos
        if self.recording:
            self.recording = False
            self.mouse_listener.stop()
            self.keyboard_listener.stop()
            self.save_recording()
            self.update_status("Gravação parada e salva")

    def choose_path(self):
        # Escolhe o caminho do arquivo para salvar
        self.filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if self.filepath:
            self.update_status(f"Caminho selecionado: {self.filepath}")

    def choose_file(self):
        # Escolhe o arquivo para reprodução
        self.filepath = filedialog.askopenfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("All files", "*.*")])
        if self.filepath:
            self.update_status(f"Arquivo selecionado: {self.filepath}")

    def save_recording(self):
        # Salva os eventos gravados no arquivo escolhido
        if self.filepath:
            with open(self.filepath, 'w') as f:
                for event in self.events:
                    f.write(f"{event}\n")
            self.update_status("Gravação salva")
        else:
            messagebox.showwarning("Aviso", "Escolha um caminho para salvar o arquivo")

    def start_playback(self):
        # Inicia a reprodução dos eventos gravados
        if self.filepath:
            self.playing = True
            self.playback_thread = threading.Thread(target=self.playback_events)
            self.playback_thread.start()
        else:
            messagebox.showwarning("Aviso", "Escolha um arquivo para reprodução")

    def playback_events(self):
        # Lê os eventos do arquivo e os reproduz
        with open(self.filepath, 'r') as f:
            lines = f.readlines()

        mouse_controller = mouse.Controller()
        keyboard_controller = keyboard.Controller()

        for line in lines:
            if not self.playing:
                break
            parts = line.strip().split()
            event_type = parts[0]
            if event_type == "Movimento":
                x, y = int(parts[2]), int(parts[3])
                mouse_controller.position = (x, y)
            elif event_type == "Pressionado":
                button = self.get_mouse_button(parts[2])
                mouse_controller.press(button)
            elif event_type == "Liberado":
                button = self.get_mouse_button(parts[2])
                mouse_controller.release(button)
            elif event_type == "Tecla":
                key_action = parts[2]
                key = self.get_key(parts[1])
                if key_action == "pressionada":
                    keyboard_controller.press(key)
                elif key_action == "liberada":
                    keyboard_controller.release(key)
            time.sleep(0.01)  # Pequeno atraso para simular o tempo entre os eventos

    def stop_playback(self):
        # Para a reprodução dos eventos
        self.playing = False

    def exit_application(self):
        # Sai da aplicação
        self.stop_playback()  # Garante que a reprodução é parada antes de sair
        self.root.quit()

    def update_status(self, message):
        # Atualiza o status atual (neste exemplo, apenas imprime)
        print(message)

    def on_click(self, x, y, button, pressed):
        # Manipulador de eventos de clique do mouse
        if self.recording and not self.paused:
            action = "Pressionado" if pressed else "Liberado"
            self.events.append(f"{action} {button.name} em {x} {y}")
            self.update_status(f"{action} {button.name} em {x} {y}")

    def on_move(self, x, y):
        # Manipulador de eventos de movimento do mouse
        if self.recording and not self.paused:
            self.events.append(f"Movimento em {x} {y}")
            self.update_status(f"Movimento em {x} {y}")

    def on_press(self, key):
        # Manipulador de eventos de pressionamento de teclas
        if self.recording and not self.paused:
            key_name = key.name if isinstance(key, keyboard.Key) else str(key)
            self.events.append(f"Tecla {key_name} pressionada")
            self.update_status(f"Tecla {key_name} pressionada")

    def on_release(self, key):
        # Manipulador de eventos de liberação de teclas
        if self.recording and not self.paused:
            key_name = key.name if isinstance(key, keyboard.Key) else str(key)
            self.events.append(f"Tecla {key_name} liberada")
            self.update_status(f"Tecla {key_name} liberada")

    def get_mouse_button(self, button_name):
        # Obtém o botão do mouse a partir do nome
        try:
            return mouse.Button[button_name.lower()]
        except KeyError:
            return mouse.Button.left  # Padrão para o botão esquerdo

    def get_key(self, key_name):
        # Obtém a tecla do teclado a partir do nome
        try:
            return keyboard.Key[key_name]
        except KeyError:
            return key_name  # Caso contrário, retorna o nome original

if __name__ == "__main__":
    root = tk.Tk()
    app = ClickRecorderReproducer(root)
    root.mainloop()
