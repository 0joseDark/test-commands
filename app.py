import tkinter as tk
from tkinter import messagebox
from datetime import datetime
import os

# Nome do arquivo para gravar os comandos
command_file = "commands.txt"

# Função para verificar se o arquivo existe, se não, cria
def ensure_file_exists():
    if not os.path.exists(command_file):
        with open(command_file, "w") as file:
            file.write("Arquivo de comandos criado.\n")

# Função para gravar os comandos no arquivo
def log_command(command):
    if recording:
        with open(command_file, "a") as file:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp}: {command}\n")

# Função para alterar a cor do botão e registrar o comando
def on_button_click(button, command):
    button.configure(bg="green")
    log_command(command)

    # Retorna à cor original após um tempo
    button.after(200, lambda: button.configure(bg="SystemButtonFace"))

# Função para ler e reproduzir os comandos do arquivo
def replay_commands():
    try:
        with open(command_file, "r") as file:
            for line in file:
                print(line.strip())
    except FileNotFoundError:
        print("Nenhum comando gravado ainda.")

# Função para iniciar a gravação
def start_recording():
    global recording
    recording = True
    lbl_status.config(text="Gravando...")

# Função para pausar a gravação
def pause_recording():
    global recording
    recording = False
    lbl_status.config(text="Pausado")

# Função para parar a gravação
def stop_recording():
    global recording
    recording = False
    lbl_status.config(text="Parado")

# Função para sair do aplicativo
def exit_application():
    root.destroy()

# Criando a janela principal
root = tk.Tk()
root.title("Controle com Setas")

# Variável global para controlar a gravação
recording = False

# Assegura que o arquivo existe
ensure_file_exists()

# Criando os botões
btn_up = tk.Button(root, text="↑", width=10, height=2, command=lambda: on_button_click(btn_up, "UP"))
btn_down = tk.Button(root, text="↓", width=10, height=2, command=lambda: on_button_click(btn_down, "DOWN"))
btn_left = tk.Button(root, text="←", width=10, height=2, command=lambda: on_button_click(btn_left, "LEFT"))
btn_right = tk.Button(root, text="→", width=10, height=2, command=lambda: on_button_click(btn_right, "RIGHT"))

# Posicionando os botões em forma de cruz
btn_up.grid(row=0, column=1)
btn_down.grid(row=2, column=1)
btn_left.grid(row=1, column=0)
btn_right.grid(row=1, column=2)

# Botões adicionais
btn_start = tk.Button(root, text="Ligar", command=start_recording)
btn_pause = tk.Button(root, text="Pausa", command=pause_recording)
btn_stop = tk.Button(root, text="Parar", command=stop_recording)
btn_exit = tk.Button(root, text="Sair", command=exit_application)

# Posicionando botões adicionais
btn_start.grid(row=3, column=0, pady=10)
btn_pause.grid(row=3, column=1, pady=10)
btn_stop.grid(row=3, column=2, pady=10)
btn_exit.grid(row=4, column=1, pady=10)

# Botão para reproduzir os comandos
btn_replay = tk.Button(root, text="Reproduzir Comandos", command=replay_commands)
btn_replay.grid(row=4, column=0, pady=10)

# Label para exibir o status
lbl_status = tk.Label(root, text="Parado")
lbl_status.grid(row=4, column=2, pady=10)

# Rodar a aplicação
root.mainloop()
