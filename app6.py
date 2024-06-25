import tkinter as tk
from datetime import datetime, timedelta
import os
import pyautogui
import pygetwindow as gw

# Nome do arquivo para gravar os comandos
command_file = "commands.txt"

# Variáveis globais
start_time = None
last_command_time = None
recording = False
target_window = None

# Função para verificar se o arquivo existe, se não, cria
def ensure_file_exists():
    if not os.path.exists(command_file):
        with open(command_file, "w") as file:
            file.write("Arquivo de comandos criado.\n")

# Função para calcular o tempo decorrido desde o último comando
def get_time_since_last_command():
    global last_command_time
    if last_command_time:
        elapsed = datetime.now() - last_command_time
        hours, remainder = divmod(elapsed.total_seconds(), 3600)
        minutes, seconds = divmod(remainder, 60)
        return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"
    else:
        return "0h 0m 0s"

# Função para gravar os comandos no arquivo
def log_command(command):
    global last_command_time
    if recording:
        with open(command_file, "a") as file:
            elapsed_time = get_time_since_last_command()
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            file.write(f"{timestamp} | Tempo desde último comando: {elapsed_time} | Comando: {command}\n")
        last_command_time = datetime.now()

# Função para simular a tecla e registrar o comando
def on_button_click(button, command, key):
    global target_window
    button.configure(bg="green")
    log_command(command)
    if target_window:
        target_window.activate()
        pyautogui.press(key)
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
    global recording, start_time, last_command_time
    if not recording:
        start_time = datetime.now()
        last_command_time = start_time
        recording = True
        lbl_status.config(text="Gravando...")

# Função para pausar a gravação
def pause_recording():
    global recording
    if recording:
        recording = False
        lbl_status.config(text="Pausado")

# Função para parar a gravação
def stop_recording():
    global recording, start_time, last_command_time
    if recording:
        recording = False
        start_time = None
        last_command_time = None
        lbl_status.config(text="Parado")

# Função para sair do aplicativo
def exit_application():
    root.destroy()

# Função para listar e atualizar janelas
def list_windows():
    listbox_windows.delete(0, tk.END)
    windows = gw.getWindowsWithTitle("")
    for window in windows:
        if window.isVisible and not window.isMinimized:
            listbox_windows.insert(tk.END, window.title)

# Função para selecionar a janela alvo
def select_window():
    global target_window
    selection = listbox_windows.curselection()
    if selection:
        selected_title = listbox_windows.get(selection[0])
        windows = gw.getWindowsWithTitle(selected_title)
        if windows:
            target_window = windows[0]
            lbl_window_status.config(text=f"Janela alvo: {target_window.title}")
        else:
            lbl_window_status.config(text="Janela não encontrada")
    else:
        lbl_window_status.config(text="Selecione uma janela")

# Criando a janela principal
root = tk.Tk()
root.title("Controle com Setas")

# Assegura que o arquivo existe
ensure_file_exists()

# Criando os botões de direção
btn_up = tk.Button(root, text="↑", width=10, height=2, command=lambda: on_button_click(btn_up, "UP", "up"))
btn_down = tk.Button(root, text="↓", width=10, height=2, command=lambda: on_button_click(btn_down, "DOWN", "down"))
btn_left = tk.Button(root, text="←", width=10, height=2, command=lambda: on_button_click(btn_left, "LEFT", "left"))
btn_right = tk.Button(root, text="→", width=10, height=2, command=lambda: on_button_click(btn_right, "RIGHT", "right"))

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
btn_start.grid(row=4, column=0, pady=10)
btn_pause.grid(row=4, column=1, pady=10)
btn_stop.grid(row=4, column=2, pady=10)
btn_exit.grid(row=5, column=1, pady=10)

# Botão para reproduzir os comandos
btn_replay = tk.Button(root, text="Reproduzir Comandos", command=replay_commands)
btn_replay.grid(row=5, column=0, pady=10)

# Label para exibir o status
lbl_status = tk.Label(root, text="Parado")
lbl_status.grid(row=5, column=2, pady=10)

# Lista de janelas
listbox_windows = tk.Listbox(root, height=6, width=40)
listbox_windows.grid(row=0, column=3, rowspan=3, padx=10)
btn_refresh_windows = tk.Button(root, text="Atualizar Janelas", command=list_windows)
btn_refresh_windows.grid(row=3, column=3, pady=10)
btn_select_window = tk.Button(root, text="Selecionar Janela", command=select_window)
btn_select_window.grid(row=4, column=3, pady=10)
lbl_window_status = tk.Label(root, text="Nenhuma janela selecionada")
lbl_window_status.grid(row=5, column=3, pady=10)

# Inicializar a lista de janelas
list_windows()

# Rodar a aplicação
root.mainloop()
