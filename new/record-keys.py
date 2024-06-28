import tkinter as tk
from tkinter import filedialog
import keyboard
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

janela = tk.Tk()
janela.title("Gravador de Teclas")
janela.geometry("300x150")

btn_gravar = tk.Button(janela, text="Iniciar Gravação", command=gravar_teclas)
btn_gravar.pack(pady=20)

label_status = tk.Label(janela, text="")
label_status.pack()

janela.mainloop()