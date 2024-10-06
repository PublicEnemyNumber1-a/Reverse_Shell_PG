import tkinter as tk
from PIL import Image, ImageTk
import keyboard  # Global keyboard hook
import sys
import os

# Variável global para controlar se o programa deve continuar rodando
running = True
gif_displayed = False
root = None

def resource_path(relative_path):
    """ Retorna o caminho absoluto para o recurso, independente se for empacotado ou não. """
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

def disable_keys():
    keyboard.block_key('windows')
    keyboard.block_key('esc')
    keyboard.block_key('alt')
    keyboard.block_key('f4')
    keyboard.block_key('tab')

def enable_keys():
    keyboard.unblock_key('windows')
    keyboard.unblock_key('esc')
    keyboard.unblock_key('alt')
    keyboard.unblock_key('f4')
    keyboard.unblock_key('tab')

def display_gif():
    """ Exibe um GIF em tela cheia. """
    global gif_displayed, root
    gif_displayed = True

    # Configurações da janela principal
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.attributes("-fullscreen", True)
    root.config(cursor="none", bg="black")

    # Desabilitar teclas
    disable_keys()

    # Carregar o GIF
    gif_path = resource_path("hack3.gif")
    gif_image = Image.open(gif_path)
    gif_frames = []

    # Redimensionar frames do GIF
    for frame_index in range(gif_image.n_frames):
        gif_image.seek(frame_index)
        resized_frame = gif_image.copy().resize((screen_width, screen_height), Image.LANCZOS)
        gif_frames.append(ImageTk.PhotoImage(resized_frame.convert('RGBA')))

    gif_label = tk.Label(root, bg="black")
    gif_label.pack(expand=True)

    # Função para reproduzir o GIF
    def play_gif(frame_index=0):
        if running and gif_displayed:  # Verifica se o programa deve continuar
            gif_label.config(image=gif_frames[frame_index])
            frame_index = (frame_index + 1) % len(gif_frames)
            gif_label.after(gif_image.info['duration'], play_gif, frame_index)

    # Substitui o comportamento padrão de fechamento da janela
    root.protocol("WM_DELETE_WINDOW", lambda: stop_program())

    # Iniciar a reprodução do GIF
    play_gif()
    root.mainloop()

def stop_program():
    """ Função para parar o programa. """
    global running, gif_displayed
    running = False
    gif_displayed = False
    if root:
        root.destroy()  # Fecha a janela principal
        enable_keys()

def close_program():
    """ Closes the program using os._exit(). """
    global running
    running = False
    os._exit(0)  # Terminate the program
        

def open_gif():
    """ Função para abrir o GIF. """
    if not gif_displayed:  # Verifica se o GIF já está exibido
        display_gif()

def close_gif():
    """ Função para fechar o GIF. """
    stop_program()

def main_loop():
    """ Loop principal que escuta as teclas. """
    global running
    while running:
        if keyboard.is_pressed('open'):
            open_gif()
        elif keyboard.is_pressed('close'):
            close_gif()

if __name__ == "__main__":
    running = True
    main_loop()
