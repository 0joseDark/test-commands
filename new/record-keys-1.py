import os
import tkinter as tk
from tkinter import filedialog
from pynput import mouse, keyboard
import time

# Variáveis globais
log_file_path = ""  # Caminho do ficheiro de log
log_data = []       # Armazena os eventos para reproduzir depois

# Função para escolher o caminho do log
def escolher_caminho():
    global log_file_path
    log_file_path = filedialog.asksaveasfilename(defaultextension=".log", filetypes=[("Log Files", "*.log")])
    if log_file_path:
        print(f"Caminho escolhido: {log_file_path}")

# Função para gravar no log
def gravar_no_log(evento):
    global log_file_path
    if log_file_path:
        with open(log_file_path, "a") as f:
            f.write(evento + "\n")
            print(f"Gravado: {evento}")

# Função que regista o clique do rato
def on_click(x, y, button, pressed):
    if pressed:
        evento = f"Click,{x},{y},{button}"
        gravar_no_log(evento)

# Função que regista os movimentos do rato
def on_move(x, y):
    evento = f"Move,{x},{y}"
    gravar_no_log(evento)

# Função que regista as teclas pressionadas
def on_press(key):
    try:
        if key in [keyboard.Key.up, keyboard.Key.down, keyboard.Key.left, keyboard.Key.right, 
                   keyboard.Key.page_up, keyboard.Key.page_down]:
            evento = f"Tecla,{key}"
            gravar_no_log(evento)
    except AttributeError:
        pass

# Função para iniciar o monitoramento do rato e teclado
def iniciar_monitoramento():
    global listener_mouse, listener_teclado
    # Iniciar o listener de rato
    listener_mouse = mouse.Listener(on_click=on_click, on_move=on_move)
    listener_mouse.start()
    
    # Iniciar o listener de teclado
    listener_teclado = keyboard.Listener(on_press=on_press)
    listener_teclado.start()

# Função para parar o monitoramento
def parar_monitoramento():
    listener_mouse.stop()
    listener_teclado.stop()

# Função para ler e reproduzir os eventos do log
def reproduzir_eventos():
    global log_file_path
    if log_file_path and os.path.exists(log_file_path):
        with open(log_file_path, "r") as f:
            log_data = f.readlines()
        
        for evento in log_data:
            evento = evento.strip().split(",")
            if evento[0] == "Move":
                x, y = int(evento[1]), int(evento[2])
                print(f"Movendo rato para ({x}, {y})")
                # Simular movimento do rato (pode usar `pyautogui` ou outra lib)
                # pyautogui.moveTo(x, y)
                
            elif evento[0] == "Click":
                x, y, button = int(evento[1]), int(evento[2]), evento[3]
                print(f"Clique em ({x}, {y}) com {button}")
                # Simular clique do rato
                
            elif evento[0] == "Tecla":
                tecla = evento[1]
                print(f"Tecla pressionada: {tecla}")
                # Simular tecla pressionada

# Criar a janela principal
janela = tk.Tk()
janela.title("Monitor de Rato e Teclado")

# Criar os botões
btn_escolher_caminho = tk.Button(janela, text="Escolher caminho do log", command=escolher_caminho)
btn_iniciar = tk.Button(janela, text="Iniciar Monitoramento", command=iniciar_monitoramento)
btn_parar = tk.Button(janela, text="Parar Monitoramento", command=parar_monitoramento)
btn_reproduzir = tk.Button(janela, text="Reproduzir Eventos", command=reproduzir_eventos)
btn_sair = tk.Button(janela, text="Sair", command=janela.quit)

# Posicionar os botões
btn_escolher_caminho.pack(pady=5)
btn_iniciar.pack(pady=5)
btn_parar.pack(pady=5)
btn_reproduzir.pack(pady=5)
btn_sair.pack(pady=5)

# Iniciar o loop da interface gráfica
janela.mainloop()
