import tkinter as tk
from tkinter import filedialog
import keyboard
import pyautogui
import time
import os

def gravar_teclas():
    arquivo = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Arquivo de Texto", "*.txt")])
    if not arquivo:
        return

    label_status.config(text="Gravando... Pressione ESC para parar.")
    
    with open(arquivo, "w") as f:
        while True:
            evento = keyboard.read_event(suppress=True)
            if evento.event_type == keyboard.KEY_DOWN:
                if evento.name == "esc":
                    break
                elif evento.name in ["up", "down", "left", "right"]:
                    f.write(evento.name + "\n")
                    f.flush()
    
    label_status.config(text="Gravação finalizada.")

def executar_comandos():
    arquivo = filedialog.askopenfilename(filetypes=[("Arquivo de Texto", "*.txt")])
    if not arquivo:
        return

    label_status.config(text="Executando comandos...")
    
    with open(arquivo, "r") as f:
        comandos = f.readlines()

    for comando in comandos:
        comando = comando.strip()
        if comando in ["up", "down", "left", "right"]:
            pyautogui.press(comando)
            time.sleep(0.1)  # Pequena pausa entre comandos

    label_status.config(text="Execução finalizada.")

def sair():
    janela.quit()

janela = tk.Tk()
janela.title("Gravador e Executor de Teclas")
janela.geometry("300x200")

btn_gravar = tk.Button(janela, text="Iniciar Gravação", command=gravar_teclas)
btn_gravar.pack(pady=10)

btn_executar = tk.Button(janela, text="Executar Comandos", command=executar_comandos)
btn_executar.pack(pady=10)

btn_sair = tk.Button(janela, text="Sair", command=sair)
btn_sair.pack(pady=10)

label_status = tk.Label(janela, text="")
label_status.pack()

janela.mainloop()