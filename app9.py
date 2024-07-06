# pip install pyautogui pygetwindow

import pyautogui  # Biblioteca para controle de teclado e mouse
import pygetwindow as gw  # Biblioteca para manipulação de janelas
import time  # Biblioteca para manipulação de tempo
import tkinter as tk  # Biblioteca para a interface gráfica
from tkinter import ttk  # Biblioteca para a interface gráfica (widgets temáticos)
import os  # Biblioteca para manipulação de arquivos e sistema operacional

class MemoriaComandos:
    def __init__(self, log_file='comandos.log'):
        self.comandos = []  # Lista para armazenar comandos
        self.log_file = log_file  # Nome do arquivo de log
        self.carregar_comandos()  # Carregar comandos do arquivo de log

    def adicionar_comando(self, comando):
        # Adiciona um comando à memória e ao arquivo de log
        self.comandos.append(comando)
        print(f"Comando adicionado: {comando}")
        with open(self.log_file, 'a') as f:
            f.write(f"{comando[0]},{comando[1]}\n")

    def carregar_comandos(self):
        # Carrega comandos do arquivo de log, se existir
        if os.path.exists(self.log_file):
            with open(self.log_file, 'r') as f:
                for linha in f:
                    tecla, atraso = linha.strip().split(',')
                    self.comandos.append((tecla, float(atraso)))
            print(f"Comandos carregados do log: {self.comandos}")

    def reproduzir_comandos(self):
        # Reproduz os comandos armazenados na memória
        print("Reproduzindo comandos...")
        for comando in self.comandos:
            tecla, atraso = comando
            pyautogui.press(tecla)
            print(f"Pressionou a tecla: {tecla}")
            time.sleep(atraso)

def janela_ativa(nome_janela):
    # Verifica se a janela com o título fornecido está ativa
    janelas = gw.getWindowsWithTitle(nome_janela)
    return any(janela.isActive for janela in janelas)

def obter_janelas():
    # Retorna uma lista de títulos de todas as janelas visíveis
    return [janela.title for janela in gw.getAllTitles() if janela]

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Controlador de Janela")
        self.memoria = MemoriaComandos()

        # Configuração da GUI
        self.label_janela = ttk.Label(root, text="Selecionar Janela:")
        self.label_janela.grid(row=0, column=0, padx=10, pady=10)

        self.combo_janela = ttk.Combobox(root, values=obter_janelas())
        self.combo_janela.grid(row=0, column=1, padx=10, pady=10)

        self.btn_atualizar = ttk.Button(root, text="Atualizar Janelas", command=self.atualizar_janelas)
        self.btn_atualizar.grid(row=0, column=2, padx=10, pady=10)

        # Botões para adicionar comandos
        self.btn_up = ttk.Button(root, text="Up", command=lambda: self.adicionar_comando('up'))
        self.btn_up.grid(row=1, column=0, padx=10, pady=10)

        self.btn_down = ttk.Button(root, text="Down", command=lambda: self.adicionar_comando('down'))
        self.btn_down.grid(row=1, column=1, padx=10, pady=10)

        self.btn_left = ttk.Button(root, text="Left", command=lambda: self.adicionar_comando('left'))
        self.btn_left.grid(row=1, column=2, padx=10, pady=10)

        self.btn_right = ttk.Button(root, text="Right", command=lambda: self.adicionar_comando('right'))
        self.btn_right.grid(row=1, column=3, padx=10, pady=10)

        self.btn_pageup = ttk.Button(root, text="Page Up", command=lambda: self.adicionar_comando('pageup'))
        self.btn_pageup.grid(row=2, column=0, padx=10, pady=10)

        self.btn_pagedown = ttk.Button(root, text="Page Down", command=lambda: self.adicionar_comando('pagedown'))
        self.btn_pagedown.grid(row=2, column=1, padx=10, pady=10)

        # Botão para iniciar a reprodução dos comandos
        self.btn_reproduzir = ttk.Button(root, text="Reproduzir Comandos", command=self.reproduzir_comandos)
        self.btn_reproduzir.grid(row=3, column=0, columnspan=4, pady=20)

    def atualizar_janelas(self):
        # Atualiza a lista de janelas disponíveis na combobox
        self.combo_janela['values'] = obter_janelas()

    def adicionar_comando(self, tecla):
        # Adiciona um comando com a tecla especificada e um atraso fixo de 1 segundo
        atraso = 1
        self.memoria.adicionar_comando((tecla, atraso))

    def reproduzir_comandos(self):
        # Reproduz os comandos quando a janela alvo estiver ativa
        nome_janela_alvo = self.combo_janela.get()
        if not nome_janela_alvo:
            print("Nenhuma janela selecionada.")
            return
        print(f"Esperando a janela '{nome_janela_alvo}' ficar ativa...")
        while not janela_ativa(nome_janela_alvo):
            time.sleep(2)
        print(f"Janela '{nome_janela_alvo}' ativa. Reproduzindo comandos...")
        self.memoria.reproduzir_comandos()

def main():
    # Cria a janela principal da GUI e inicia o loop principal
    root = tk.Tk()
    app = App(root)
    root.mainloop()

if __name__ == "__main__":
    main()
