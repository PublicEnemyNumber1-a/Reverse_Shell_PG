import tkinter as tk
from tkinter import ttk

def create_window():
    # Criar a janela principal
    window = tk.Tk()
    window.title("Futuristic Interface")
    window.geometry("400x300")

    # Definir as cores da interface
    bg_color = "#000000"  # Cor de fundo preta
    fg_color = "#ffffff"  # Cor do texto branco

    # Configurar o estilo da janela
    window.configure(bg=bg_color)

    # Criar um estilo personalizado para os widgets
    style = ttk.Style()
    style.theme_use("default")
    style.configure("TLabel", background=bg_color, foreground=fg_color, font=("Arial", 12))
    style.configure("TButton", background=bg_color, foreground=fg_color, font=("Arial", 12, "bold"), borderwidth=0, relief="flat")
    style.map("TButton",
              background=[("active", bg_color), ("pressed", bg_color)],
              foreground=[("active", fg_color), ("pressed", fg_color)])

    # Adicionar um título estilizado
    title_label = ttk.Label(window, text="AI is in silent mode", font=("Arial", 18, "bold"))
    title_label.pack(pady=20)

    # Adicionar um botão de fechar estilizado
    def close_window():
        window.destroy()

    close_button = ttk.Button(window, text="Close", command=close_window)
    close_button.pack(pady=10)

    # Iniciar o loop principal da janela
    window.mainloop()

def main2():
    create_window()

if __name__ == "__main__":
    main2()