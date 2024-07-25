import pyautogui
import pygetwindow as gw
import tkinter as tk
from tkinter import ttk
import logging
import time

# Configurar o sistema de log
logging.basicConfig(filename='key_commands.log', level=logging.INFO, format='%(asctime)s:%(message)s')

# Funções para enviar comandos de teclas e mouse
def send_key_command(key):
    """Envia um comando de tecla simulando a pressionar uma tecla"""
    pyautogui.press(key)
    logging.info(f'Key press: {key}')  # Log da ação

def send_mouse_click(x, y):
    """Envia um comando de clique do mouse em uma posição (x, y)"""
    pyautogui.click(x, y)
    logging.info(f'Mouse click at: ({x}, {y})')  # Log da ação

def send_mouse_move(x, y):
    """Move o mouse para uma posição (x, y)"""
    pyautogui.moveTo(x, y)
    logging.info(f'Mouse move to: ({x}, {y})')  # Log da ação

def replay_commands(window_title):
    """Reproduz os comandos armazenados no log, se a janela alvo estiver ativa"""
    target_window = gw.getWindowsWithTitle(window_title)
    if not target_window:
        print(f"A janela '{window_title}' não está ativa ou não foi encontrada.")
        return

    target_window = target_window[0]

    with open('key_commands.log', 'r') as log_file:
        for line in log_file:
            timestamp, command = line.strip().split(':', 1)
            if 'Key press' in command:
                key = command.split(':')[-1].strip()
                if target_window.isActive:
                    pyautogui.press(key)
            elif 'Mouse click' in command:
                x, y = map(int, command.split(':')[-1].strip()[1:-1].split(','))
                if target_window.isActive:
                    pyautogui.click(x, y)
            elif 'Mouse move' in command:
                x, y = map(int, command.split(':')[-1].strip()[1:-1].split(','))
                if target_window.isActive:
                    pyautogui.moveTo(x, y)
            time.sleep(0.1)  # Pausa para garantir que a ação seja reproduzida corretamente

# Funções auxiliares para a GUI
def list_active_windows():
    """Lista os títulos das janelas ativas"""
    windows = gw.getAllTitles()
    return [win for win in windows if win]  # Remove entradas vazias

def execute_commands():
    """Executa comandos de exemplo"""
    if not target_window_title.get():
        print("Selecione uma janela alvo.")
        return

    send_key_command('up')    # Pressiona seta para cima
    send_key_command('down')  # Pressiona seta para baixo
    send_key_command('left')  # Pressiona seta para a esquerda
    send_key_command('right') # Pressiona seta para a direita
    send_key_command('pgup')  # Pressiona Page Up
    send_key_command('pgdn')  # Pressiona Page Down
    send_mouse_click(100, 200) # Clique do mouse em (100, 200)
    send_mouse_move(300, 400)  # Move o mouse para (300, 400)

def start_replay():
    """Inicia a reprodução dos comandos"""
    if not target_window_title.get():
        print("Selecione uma janela alvo.")
        return
    replay_commands(target_window_title.get())

def close_app():
    """Fecha a aplicação"""
    root.quit()

# Criar a interface gráfica
root = tk.Tk()
root.title("Controlador de Teclas e Mouse")

# Frame principal
main_frame = ttk.Frame(root, padding="10")
main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Título do menu
ttk.Label(main_frame, text="Selecione a Janela Alvo:", font=("Arial", 12)).grid(row=0, column=0, pady=5, sticky=tk.W)

# Dropdown para seleção de janela
target_window_title = tk.StringVar()
windows_list = list_active_windows()
window_selector = ttk.Combobox(main_frame, textvariable=target_window_title, values=windows_list, state="readonly", width=50)
window_selector.grid(row=1, column=0, pady=5)

# Botão para executar comandos
ttk.Button(main_frame, text="Executar Comandos", command=execute_commands).grid(row=2, column=0, pady=5, sticky=tk.W)

# Botão para reproduzir comandos
ttk.Button(main_frame, text="Reproduzir Comandos Gravados", command=start_replay).grid(row=3, column=0, pady=5, sticky=tk.W)

# Botão para sair
ttk.Button(main_frame, text="Sair", command=close_app).grid(row=4, column=0, pady=5, sticky=tk.W)

# Atualizar a lista de janelas ao abrir o menu
def update_window_list(event):
    windows_list = list_active_windows()
    window_selector['values'] = windows_list

window_selector.bind("<Button-1>", update_window_list)

root.mainloop()
