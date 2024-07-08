# Importar bibliotecas necessárias
import pyautogui
import pynput
import pygetwindow as gw
import logging
import time

# 1. Configurar o sistema de log
logging.basicConfig(filename='key_commands.log', level=logging.INFO, format='%(asctime)s:%(message)s')

# 2. Funções para enviar comandos de teclas e mouse
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

# 3. Função para reproduzir os comandos do log
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

# 4. Função principal de exemplo
def main():
    # Defina o título da janela alvo
    target_window_title = 'Alvo'

    # Exemplo de envio de comandos
    send_key_command('up')    # Pressiona seta para cima
    send_key_command('down')  # Pressiona seta para baixo
    send_key_command('left')  # Pressiona seta para a esquerda
    send_key_command('right') # Pressiona seta para a direita
    send_key_command('pgup')  # Pressiona Page Up
    send_key_command('pgdn')  # Pressiona Page Down
    send_mouse_click(100, 200) # Clique do mouse em (100, 200)
    send_mouse_move(300, 400)  # Move o mouse para (300, 400)

    # Espera um momento e depois reproduz os comandos
    time.sleep(5)
    replay_commands(target_window_title)

if __name__ == '__main__':
    main()
