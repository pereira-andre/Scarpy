# main.py

import tkinter as tk
from gui.gui import MainGUI


def main():
    """
    Função principal para iniciar a interface gráfica do usuário.
    """
    # Cria a janela principal da aplicação Tkinter
    root = tk.Tk()

    # Inicializa a interface gráfica definida em gui.py
    app = MainGUI(root)

    # Inicia o loop principal da interface gráfica
    root.mainloop()


if __name__ == "__main__":
    main()
