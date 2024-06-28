import tkinter as tk
from tkinter import filedialog
import pyautogui
import time

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

janela = tk.Tk()
janela.title("Executor de Comandos")
janela.geometry("300x150")

btn_executar = tk.Button(janela, text="Executar Comandos", command=executar_comandos)
btn_executar.pack(pady=20)

label_status = tk.Label(janela, text="")
label_status.pack()

janela.mainloop()