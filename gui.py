# gui.py

from scraper_controller import ScraperController
import data_analysis
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage, Toplevel
import requests


class MainGUI:
    """ Classe principal da interface gráfica do usuário para o aplicativo SCARPY. """

    def __init__(self, root):
        """ Inicializa a janela principal. """
        self.root = root
        self.root.title("SCARPY - Automotive Data Collection & Analysis App")
        self.root.configure(bg='#07171c')
        self.initialize_gui()
        self.scraper = None

    def initialize_gui(self):
        """ Configura os componentes iniciais da interface gráfica. """
        self.add_top_image()
        self.add_buttons_to_menu()

    def add_top_image(self):
        """ Adiciona uma imagem no topo da janela. """
        self.image = PhotoImage(file='logo.png')  # Caminho para a imagem do logo
        self.image_label = tk.Label(self.root, image=self.image, bg='#07171c')
        self.image_label.pack(pady=10)

    def add_buttons_to_menu(self):
        """ Adiciona botões ao menu principal. """
        self.buttons_frame = tk.Frame(self.root, bg='#07171c')
        self.buttons_frame.pack(fill='x', padx=20)
        self.create_menu_buttons()

    def create_menu_buttons(self):
        """ Cria botões individuais no menu. """
        buttons_info = [
            ("Recolher dados", self.open_scraping_config),
            ("Analisar Dados", self.analyze_data),
            ("Melhores Resultados", self.placeholder_function),
            ("Simular crédito", self.placeholder_function),
            ("Instruções", self.placeholder_function),
            ("Créditos", self.credits),
            ("Atualizações", self.check_for_updates),
            ("Sair", self.quit)
        ]

        for text, command in buttons_info:
            button = tk.Button(self.buttons_frame, text=text, command=command, bg='white', fg='black')
            button.pack(fill='x', pady=5)

    def open_scraping_config(self):
        """Abre a janela de configuração do scraper."""
        self.config_window = Toplevel(self.root)
        self.config_window.title("Configuração do Scraper")
        self.config_window.configure(bg='#07171c')
        self.config_window.geometry("400x250")

        # Iniciar a configuração da Página Inicial e Página Final
        self.start_page_label = tk.Label(self.config_window, text="Página Inicial:", bg='#07171c', fg='white')
        self.start_page_label.pack(pady=5)
        self.start_page_entry = tk.Entry(self.config_window)
        self.start_page_entry.pack()
        self.start_page_entry.insert(0, "1")  # Valor padrão para a página inicial

        self.end_page_label = tk.Label(self.config_window, text="Página Final:", bg='#07171c', fg='white')
        self.end_page_label.pack(pady=5)
        self.end_page_entry = tk.Entry(self.config_window)
        self.end_page_entry.pack()
        self.end_page_entry.insert(0, "1")  # Valor padrão para a página final

        # Configuração para o tempo de espera (Sleep Time)
        self.sleep_label = tk.Label(self.config_window, text="Sleep time (min-max):", bg='#07171c', fg='white')
        self.sleep_label.pack(pady=5)
        self.sleep_frame = tk.Frame(self.config_window, bg='#07171c')
        self.sleep_frame.pack(pady=5)
        self.sleep_min_entry = tk.Entry(self.sleep_frame, width=5)
        self.sleep_min_entry.pack(side=tk.LEFT, padx=5)
        self.sleep_min_entry.insert(0, "3")  # Valor padrão mínimo
        self.sleep_max_entry = tk.Entry(self.sleep_frame, width=5)
        self.sleep_max_entry.pack(side=tk.RIGHT, padx=5)
        self.sleep_max_entry.insert(0, "6")  # Valor padrão máximo

        self.start_scraping_button = tk.Button(self.config_window, text="Iniciar Scraping",
                                               command=self.toggle_scraping, bg='white', fg='black')
        self.start_scraping_button.pack(pady=10)

        self.scraping_in_progress = False


    def toggle_scraping(self):
        if not self.scraping_in_progress:
            self.start_scraping()
        else:
            self.stop_scraping()

    def start_scraping(self):
        start_page = int(self.start_page_entry.get())
        end_page = int(self.end_page_entry.get())
        min_sleep = int(self.sleep_min_entry.get())
        max_sleep = int(self.sleep_max_entry.get())

        # Verificação se o número da página final é menor que o número da página inicial
        if end_page < start_page:
            messagebox.showerror("Erro de Configuração",
                                 "A página final deve ser maior ou igual à página inicial.")
            return

        self.scraper = ScraperController()

        def scraping_thread_function():
            message = self.scraper.run(start_page, end_page, min_sleep, max_sleep)
            messagebox.showinfo("Status do Scraping", message)
            self.update_button_text("Iniciar Scraping")  # Adicione esta linha

        # Criação e início da thread
        scraping_thread = threading.Thread(target=scraping_thread_function, daemon=True)
        scraping_thread.start()

        # Atualizar o estado para indicar que o scraping está em progresso
        self.scraping_in_progress = True
        self.start_scraping_button.config(text="Parar Scraping")

    def update_button_text(self, text):
        """Atualiza o texto do botão de scraping."""
        self.start_scraping_button.config(text=text)

    def stop_scraping(self):
        if self.scraping_in_progress and hasattr(self, 'scraper'):
            self.scraper.stop()  # Chama o método stop
            self.scraping_in_progress = False
            self.start_scraping_button.config(text="Iniciar Scraping")

    def run_scraping(self, num_pages, min_sleep, max_sleep):
        self.scraper = ScraperController()  # Mantenha a instância do ScraperController
        try:
            self.scraper.run(max_pages=num_pages)
            if not self.scraper.interrupted:
                messagebox.showinfo("Concluído", "Scraping concluído com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Ocorreu um erro durante o scraping: {e}")
        finally:
            self.config_window.destroy()

    def stop_scraping(self):
        if hasattr(self, 'scraper') and self.scraping_in_progress:
            self.scraper.stop()  # Interrompe o processo de scraping
            self.scraping_in_progress = False
            self.start_scraping_button.config(text="Iniciar Scraping")

    def update_progress(self, value):
        self.progress['value'] = value
        self.root.update_idletasks()  # Atualiza a interface gráfica

    def analyze_data(self):
        """ Abre a janela para análise de dados. """
        self.analysis_window = Toplevel(self.root)
        self.analysis_window.title("Análise de Dados")
        self.analysis_window.configure(bg='#07171c')
        self.analysis_window.geometry("700x600")
        self.create_csv_input_section()
        self.fuel_type_button = tk.Button(self.analysis_window, text="Distribuição de Combustível",
                                          command=self.show_fuel_distribution)
        self.fuel_type_button.pack()

    def create_csv_input_section(self):
        """ Cria a seção para entrada do arquivo CSV e botões de análise. """
        frame = tk.Frame(self.analysis_window, bg='#07171c')
        frame.pack(pady=10)

        self.csv_entry_var = tk.StringVar(value="cars.csv")
        csv_entry = tk.Entry(frame, textvariable=self.csv_entry_var, width=50)
        csv_entry.pack(side=tk.LEFT, padx=10)

        browse_button = tk.Button(frame, text="Procurar", command=self.browse_csv, bg='white', fg='black')
        browse_button.pack(side=tk.LEFT, padx=10)

        analyze_frame = tk.Frame(self.analysis_window, bg='black')
        analyze_frame.pack(pady=5)
        analyze_button = tk.Button(analyze_frame, text="Carregar e analisar", command=self.start_data_analysis, bg='white', fg='black')
        analyze_button.pack(side=tk.LEFT, padx=5)

        max_min_button = tk.Button(analyze_frame, text="Máx & Min", command=self.start_max_min_analysis, bg='white', fg='black')
        max_min_button.pack(side=tk.LEFT, padx=5)

        graph_buttons_frame = tk.Frame(self.analysis_window, bg='#07171c')
        graph_buttons_frame.pack(pady=10)

        brand_graph_button = tk.Button(graph_buttons_frame, text="Distribuição de Marcas",
                                       command=lambda: self.show_figure('brand_distribution.png'),
                                       bg='white', fg='black')
        brand_graph_button.pack(side=tk.LEFT, padx=10)

        price_graph_button = tk.Button(graph_buttons_frame, text="Distribuição de Preços",
                                       command=lambda: self.show_figure('price_distribution.png'),
                                       bg='white', fg='black')
        price_graph_button.pack(side=tk.LEFT, padx=10)

        year_price_button = tk.Button(self.analysis_window, text="Histograma Ano-Preço",
                                      command=self.show_year_price_histogram)
        year_price_button.pack()

        mileage_price_button = tk.Button(self.analysis_window, text="Histograma Quilometragem-Preço",
                                         command=self.show_mileage_price_histogram)
        mileage_price_button.pack()

    def show_fuel_distribution(self):
        """ Gera o gráfico de distribuição de combustível e o exibe. """
        csv_file = self.csv_entry_var.get()  # Obtém o caminho do arquivo CSV
        graph_path = data_analysis.save_fuel_type_distribution_figure(csv_file)  # Gera o gráfico
        self.show_figure(graph_path)

    def show_year_price_histogram(self):
        """ Exibe o histograma do ano de registro e preço. """
        csv_file = self.csv_entry_var.get()
        histogram_path = data_analysis.save_year_price_histogram(csv_file)
        self.show_figure(histogram_path)

    def show_mileage_price_histogram(self):
        """ Exibe o histograma da quilometragem e preço. """
        csv_file = self.csv_entry_var.get()
        histogram_path = data_analysis.save_mileage_price_histogram(csv_file)
        self.show_figure(histogram_path)

    def show_figure(self, figure_path):
        """ Exibe a figura especificada em uma nova janela. """
        window = Toplevel(self.root)
        window.title("Gráfico")

        # Aqui, você precisará de uma maneira de carregar e exibir a imagem.
        # Por exemplo, você pode usar PhotoImage se o arquivo estiver no formato PNG.
        try:
            image = tk.PhotoImage(file=figure_path)
            label = tk.Label(window, image=image)
            label.image = image  # Mantenha uma referência.
            label.pack()
        except Exception as e:
            messagebox.showerror("Erro", f"Não foi possível abrir o gráfico: {e}")

    def browse_csv(self):
        """ Método para procurar um arquivo CSV. """
        filename = filedialog.askopenfilename(initialdir="/", title="Selecione um arquivo CSV",
                                              filetypes=(("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")))
        if filename:
            self.csv_entry_var.set(filename)

    def start_data_analysis(self):
        """ Inicia a análise dos dados a partir do arquivo CSV selecionado. """
        csv_file = self.csv_entry_var.get()
        try:
            stats_str = data_analysis.analyze_general_data(csv_file)
            self.display_analysis_results(stats_str)
        except Exception as e:
            messagebox.showerror("Erro ao analisar", str(e))

    def display_analysis_results(self, stats_str):
        """ Exibe os resultados da análise. """
        results_window = Toplevel(self.root)
        results_window.title("Resultados da Análise")
        results_window.geometry("330x150")
        stats_text_widget = tk.Text(results_window, height=20, width=80)
        stats_text_widget.pack(pady=10)
        stats_text_widget.insert(tk.END, stats_str)
        stats_text_widget.config(state='disabled')

    def start_max_min_analysis(self):
        """ Inicia a análise de máximos e mínimos a partir do arquivo CSV selecionado. """
        csv_file = self.csv_entry_var.get()
        try:
            max_min_str = data_analysis.analyze_max_min(csv_file)
            self.display_max_min_results(max_min_str)
        except Exception as e:
            messagebox.showerror("Erro ao analisar", str(e))

    def display_max_min_results(self, max_min_str):
        """ Exibe os resultados da análise de máximos e mínimos. """
        results_window = Toplevel(self.root)
        results_window.title("Resultados da Análise de Máximos e Mínimos")
        results_window.geometry("430x280")
        results_window.configure(bg='black')

        max_min_text_widget = tk.Text(results_window, height=20, width=80)
        max_min_text_widget.pack(pady=10)
        max_min_text_widget.insert(tk.END, max_min_str)
        max_min_text_widget.config(state='disabled')

    def placeholder_function(self):
        """ Função de placeholder para funcionalidades futuras. """
        pass

    def check_for_updates(self):
        current_version = "1.0.0"  # Versão atual do programa
        version_url = "https://github.com/pereira-andre/Scarpy/tree/main/version.txt"

        try:
            response = requests.get(version_url)
            latest_version = response.text.strip()

            if latest_version != current_version:
                messagebox.showinfo("Atualização Disponível",
                                    f"Uma nova versão ({latest_version}) está disponível.\n"
                                    "Por favor, visite o repositório do GitHub para atualizar.")
            else:
                messagebox.showinfo("Sem Atualizações", "Você está utilizando a versão mais recente.")
        except Exception as e:
            messagebox.showerror("Erro ao Verificar Atualização", str(e))

    def credits(self):
        """
        Método para exibir os créditos do programa.
        """
        credits_text = (
            "Programa desenvolvido por André Marques Pereira, aluno de Licenciatura em Engenharia Informática "
            "da Universidade Aberta.\n"
            "Número de aluno: 2202880.\n\n"
            "Todos os direitos reservados. Este software foi criado para fins educacionais e não pode ser "
            "reproduzido, distribuído ou utilizado para outros fins sem o consentimento explícito do autor."
        )
        messagebox.showinfo("Créditos", credits_text)

    def quit(self):
        """ Encerra o programa. """
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()

