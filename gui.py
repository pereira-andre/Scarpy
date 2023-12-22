# gui.py

from scraper_controller import ScraperController
import data_analysis
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, PhotoImage, Toplevel
import requests
import os
import webbrowser


class MainGUI:
    """ Classe principal da interface gráfica do usuário para o aplicativo SCARPY. """

    def __init__(self, root):
        """ Inicializa a janela principal. """
        self.csv_file = "cars.csv"
        self.root = root
        self.scraper = None

        # Inicialização dos atributos para armazenar as entradas do usuário
        self.detailed_report_var = tk.BooleanVar(value=False)
        self.brand_var = tk.StringVar(value="")
        self.fuel_var = tk.StringVar(value="")
        self.month_var = tk.StringVar(value="")
        self.min_year_var = tk.StringVar(value="")
        self.max_year_var = tk.StringVar(value="")
        self.year_var = tk.StringVar(value="")
        self.min_price_var = tk.StringVar(value="")
        self.max_price_var = tk.StringVar(value="")
        self.min_mileage_var = tk.StringVar(value="")
        self.max_mileage_var = tk.StringVar(value="")
        self.min_power_var = tk.StringVar(value="")
        self.max_power_var = tk.StringVar(value="")
        self.detailed_report_var = tk.BooleanVar(value=False)

        # Configuração inicial da janela principal
        self.root.title("SCARPY - Automotive Data Collection & Analysis App")
        self.root.configure(bg="#07171c")
        self.initialize_gui()

    def initialize_gui(self):
        """ Configura os componentes iniciais da interface gráfica. """
        self.add_top_image()
        self.add_buttons_to_menu()

    def add_top_image(self):
        """ Adiciona uma imagem no topo da janela. """
        self.image = PhotoImage(file="logo.png")  # Caminho para a imagem do logo
        self.image_label = tk.Label(self.root, image=self.image, bg="#07171c")
        self.image_label.pack(pady=1)

    def add_buttons_to_menu(self):
        """ Adiciona botões ao menu principal. """
        self.buttons_frame = tk.Frame(self.root, bg="#07171c")
        self.buttons_frame.pack(fill="x", padx=20)
        self.create_menu_buttons()

    def create_menu_buttons(self):
        """ Cria botões individuais no menu. """
        buttons_info = [
            ("Recolher dados", self.open_scraping_config),
            ("Analisar Dados", self.analyze_data),
            ("Instruções", self.open_instructions),
            ("Créditos", self.credits),
            ("Configurações", self.open_config_window),
            ("Atualizações", self.check_for_updates),
            ("Sair", self.quit),
        ]

        for text, command in buttons_info:
            button = tk.Button(
                self.buttons_frame, text=text, command=command, bg="white", fg="black"
            )
            button.pack(fill="x", pady=5)

    def open_scraping_config(self):
        """Abre a janela de configuração do scraper."""
        self.config_window = Toplevel(self.root)
        self.config_window.title("Configuração do Scraper")
        self.config_window.configure(bg="#07171c")
        self.config_window.geometry("400x250")

        # Iniciar a configuração da Página Inicial e Página Final
        self.start_page_label = tk.Label(
            self.config_window, text="Página Inicial:", bg="#07171c", fg="white"
        )
        self.start_page_label.pack(pady=5)
        self.start_page_entry = tk.Entry(self.config_window)
        self.start_page_entry.pack()
        self.start_page_entry.insert(0, "1")  # Valor padrão para a página inicial

        self.end_page_label = tk.Label(
            self.config_window, text="Página Final:", bg="#07171c", fg="white"
        )
        self.end_page_label.pack(pady=5)
        self.end_page_entry = tk.Entry(self.config_window)
        self.end_page_entry.pack()
        self.end_page_entry.insert(0, "1")  # Valor padrão para a página final

        # Configuração para o tempo de espera (Sleep Time)
        self.sleep_label = tk.Label(
            self.config_window, text="Sleep time (min-max):", bg="#07171c", fg="white"
        )
        self.sleep_label.pack(pady=5)
        self.sleep_frame = tk.Frame(self.config_window, bg="#07171c")
        self.sleep_frame.pack(pady=5)
        self.sleep_min_entry = tk.Entry(self.sleep_frame, width=5)
        self.sleep_min_entry.pack(side=tk.LEFT, padx=5)
        self.sleep_min_entry.insert(0, "3")  # Valor padrão mínimo
        self.sleep_max_entry = tk.Entry(self.sleep_frame, width=5)
        self.sleep_max_entry.pack(side=tk.RIGHT, padx=5)
        self.sleep_max_entry.insert(0, "6")  # Valor padrão máximo

        self.start_scraping_button = tk.Button(
            self.config_window,
            text="Iniciar Scraping",
            command=self.toggle_scraping,
            bg="white",
            fg="black",
        )
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
            messagebox.showerror(
                "Erro de Configuração",
                "A página final deve ser maior ou igual à página inicial.",
            )
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
        if self.scraping_in_progress and hasattr(self, "scraper"):
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
        if hasattr(self, "scraper") and self.scraping_in_progress:
            self.scraper.stop()  # Interrompe o processo de scraping
            self.scraping_in_progress = False
            self.start_scraping_button.config(text="Iniciar Scraping")

    def update_progress(self, value):
        self.progress["value"] = value
        self.root.update_idletasks()  # Atualiza a interface gráfica

    def analyze_data(self):
        """ Abre a janela para análise de dados. """
        self.analysis_window = Toplevel(self.root)
        self.analysis_window.title("Análise de Dados")
        self.analysis_window.configure(bg="#07171c")
        self.analysis_window.geometry("600x530")
        self.create_csv_input_section()
        self.create_report_config_section()

    def create_csv_input_section(self):
        """ Cria a seção para entrada do arquivo CSV. """
        frame = tk.Frame(self.analysis_window, bg="#07171c")
        frame.pack(pady=10)

        self.csv_entry_var = tk.StringVar(value="cars.csv")
        csv_entry = tk.Entry(frame, textvariable=self.csv_entry_var, width=50)
        csv_entry.pack(side=tk.LEFT, padx=10)

        browse_button = tk.Button(
            frame, text="Procurar", command=self.browse_csv, bg="white", fg="black"
        )
        browse_button.pack(side=tk.LEFT, padx=10)

    """ Cria a seção para configurar o relatório. """

    def create_report_config_section(self):
        """ Create the section for configuring the report. """
        config_frame = tk.Frame(self.analysis_window, bg="#07171c")
        config_frame.pack(pady=10)

        # Access the value of self.detailed_report_var to check if the checkbox is selected
        detailed_report = self.detailed_report_var.get()

        # Check if the CSV file path is defined
        if self.csv_file:
            if detailed_report:
                report_gen = data_analysis.DetailedReportGenerator(self.csv_file)
            else:
                report_gen = data_analysis.StandardReportGenerator(self.csv_file)
        else:
            messagebox.showerror("Error", "Please select a CSV file first.")

        # Marca
        brand_frame = tk.Frame(config_frame, bg="#07171c")
        brand_frame.pack(fill="x", pady=5)
        detailed_checkbox = tk.Checkbutton(
            config_frame,
            text="Relatório Detalhado",
            variable=self.detailed_report_var,
            bg="#07171c",
            fg="white",
        )
        self.create_dropdown(
            brand_frame,
            "Marca:",
            self.brand_var,
            [
                "Jaguar",
                "Unique",
                "Pagani",
                "Campagna",
                "Alfa Romeo",
                "Elfin",
                "Ferrari",
                "NIE",
                "VW",
                "Suzuki",
                "Audi",
                "Opel",
                "Volvo",
                "Mitsubishi",
                "Lobini",
                "Maserati",
                "Callaway",
                "Seat",
                "Gumpert",
                "Chevrolet",
                "Chrysler",
                "Skoda",
                "Cadillac",
                "Corvette",
                "Noble",
                "Tata",
                "Honda",
                "BMW",
                "Ford",
                "Dodge",
                "Humer",
                "Holden",
                "Bristol",
                "Porsche",
                "Maybach",
                "Lotus",
                "Toyota",
                "MB Roadcars",
                "Superformance",
                "Ascari",
                "Mini",
                "Kia",
                "Aston Martin",
                "Peugeot",
                "Saab",
                "Renault",
                "LandRover",
                "Saturn",
                "Smart",
                "Perodua",
                "Radical",
                "Ariel",
                "Brooke",
                "Ssangyong",
                "Marcos",
                "Invicta",
                "Subaru",
                "Alpina",
                "Proton",
                "Isuzu",
                "Koenigsegg",
                "Fiat",
                "Lexus",
                "Tesla",
                "SSC",
                "Hyundai",
                "Mazda",
                "Spyker",
                "Jeep",
                "Rolls Royce",
                "TVR",
                "Morgan",
                "Citroen",
                "Mercedes-Benz",
                "Westfield",
                "Nissan",
                "Caerham",
                "Daihatsu",
                "Lamborghini",
                "Shelby",
                "Vauxhal",
                "Bentley",
            ],
        )

        # Combustível
        fuel_frame = tk.Frame(config_frame, bg="#07171c")
        fuel_frame.pack(fill="x", pady=5)
        self.create_dropdown(
            fuel_frame,
            "Combustível:",
            self.fuel_var,
            [
                "Gasolina",
                "Diesel",
                "Híbrido (Gasolina)",
                "Híbrido (Diesel)",
                "Eléctrico",
                "GPL",
            ],
        )

        # Mês
        month_frame = tk.Frame(config_frame, bg="#07171c")
        month_frame.pack(fill="x", pady=5)
        self.create_dropdown(
            month_frame,
            "Mês:",
            self.month_var,
            [
                "Janeiro",
                "Fevereiro",
                "Março",
                "Abril",
                "Maio",
                "Junho",
                "Julho",
                "Agosto",
                "Setembro",
                "Outubro",
                "Novembro",
                "Dezembro",
            ],
        )

        # Ano Mínimo e Máximo
        year_frame = tk.Frame(config_frame, bg="#07171c")
        year_frame.pack(fill="x", pady=5)
        self.create_input_field(year_frame, "Ano Mínimo:", self.min_year_var)
        self.create_input_field(year_frame, "Ano Máximo:", self.max_year_var)

        # Preço Mínimo
        min_price_frame = tk.Frame(config_frame, bg="#07171c")
        min_price_frame.pack(fill="x", pady=5)
        self.create_input_field(min_price_frame, "Preço Mínimo:", self.min_price_var)

        # Preço Máximo
        max_price_frame = tk.Frame(config_frame, bg="#07171c")
        max_price_frame.pack(fill="x", pady=5)
        self.create_input_field(max_price_frame, "Preço Máximo:", self.max_price_var)

        # Quilometragem Mínima
        min_mileage_frame = tk.Frame(config_frame, bg="#07171c")
        min_mileage_frame.pack(fill="x", pady=5)
        self.create_input_field(
            min_mileage_frame, "Quilometragem Mínima:", self.min_mileage_var
        )

        # Quilometragem Máxima
        max_mileage_frame = tk.Frame(config_frame, bg="#07171c")
        max_mileage_frame.pack(fill="x", pady=5)
        self.create_input_field(
            max_mileage_frame, "Quilometragem Máxima:", self.max_mileage_var
        )

        # Potência Mínima
        min_power_frame = tk.Frame(config_frame, bg="#07171c")
        min_power_frame.pack(fill="x", pady=5)
        self.create_input_field(min_power_frame, "Potência Mínima:", self.min_power_var)

        # Potência Máxima
        max_power_frame = tk.Frame(config_frame, bg="#07171c")
        max_power_frame.pack(fill="x", pady=5)
        self.create_input_field(max_power_frame, "Potência Máxima:", self.max_power_var)

        # Checkbox para relatório detalhado
        detailed_checkbox = tk.Checkbutton(
            config_frame,
            text="Relatório Detalhado",
            variable=self.detailed_report_var,
            bg="#07171c",
            fg="white",
        )
        detailed_checkbox.pack(pady=5)

        # Botão para gerar o relatório
        generate_button = tk.Button(
            config_frame,
            text="Gerar Relatório Personalizado",
            command=self.generate_custom_report,
            bg="white",
            fg="black",
        )
        generate_button.pack(pady=10)

        if self.detailed_report_var.get():
            report_gen = data_analysis.DetailedReportGenerator(self.csv_file)
        else:
            report_gen = data_analysis.StandardReportGenerator(self.csv_file)

    def create_dropdown(self, frame, label_text, variable, options):
        label = tk.Label(frame, text=label_text, bg="#07171c", fg="white")
        label.pack(side=tk.LEFT, padx=5)
        dropdown = tk.OptionMenu(frame, variable, *options)
        dropdown.pack(side=tk.LEFT, padx=5)

    def create_input_field(self, frame, label_text, variable):
        label = tk.Label(frame, text=label_text, bg="#07171c", fg="white")
        label.pack(side=tk.LEFT, padx=5)
        entry = tk.Entry(frame, textvariable=variable, width=10)
        entry.pack(side=tk.LEFT, padx=5)

    def generate_custom_report(self):
        """ Gera um relatório personalizado com base nas entradas do usuário. """
        csv_file = self.csv_entry_var.get()  # Obter o caminho do arquivo CSV

        # Verifica se o caminho do arquivo CSV foi fornecido
        if not csv_file:
            messagebox.showerror("Erro", "Por favor, selecione um arquivo CSV.")
            return

        # Coleta os valores dos widgets de entrada
        brand = self.brand_var.get() if self.brand_var.get() else None
        fuel = self.fuel_var.get() if self.fuel_var.get() else None
        month = self.month_var.get() if self.month_var.get() else None
        min_year = (
            int(self.min_year_var.get()) if self.min_year_var.get().isdigit() else None
        )
        max_year = (
            int(self.max_year_var.get()) if self.max_year_var.get().isdigit() else None
        )
        min_price = (
            float(self.min_price_var.get()) if self.min_price_var.get() else None
        )
        max_price = (
            float(self.max_price_var.get()) if self.max_price_var.get() else None
        )
        min_mileage = (
            float(self.min_mileage_var.get()) if self.min_mileage_var.get() else None
        )
        max_mileage = (
            float(self.max_mileage_var.get()) if self.max_mileage_var.get() else None
        )
        min_power = (
            float(self.min_power_var.get()) if self.min_power_var.get() else None
        )
        max_power = (
            float(self.max_power_var.get()) if self.max_power_var.get() else None
        )
        detailed_report = self.detailed_report_var.get()

        # Escolhe o gerador de relatório baseado no tipo selecionado
        if detailed_report:
            report_gen = data_analysis.DetailedReportGenerator(csv_file)
        else:
            report_gen = data_analysis.StandardReportGenerator(csv_file)

        # Gera o relatório com os filtros aplicados
        report_path = report_gen.generate_report(
            brand=brand,
            min_year=min_year,
            max_year=max_year,
            fuel=fuel,
            month=month,
            min_price=min_price,
            max_price=max_price,
            min_mileage=min_mileage,
            max_mileage=max_mileage,
            min_power=min_power,
            max_power=max_power,
        )

        # Exibe uma mensagem com o caminho do relatório gerado
        messagebox.showinfo("Relatório Gerado", f"Relatório criado em: {report_path}")

    def browse_csv(self):
        """ Método para procurar um arquivo CSV. """
        filename = filedialog.askopenfilename(
            initialdir="/",
            title="Selecione um arquivo CSV",
            filetypes=(("Arquivos CSV", "*.csv"), ("Todos os arquivos", "*.*")),
        )
        if filename:
            self.csv_entry_var.set(filename)
            self.csv_file = filename

    def open_instructions(self):
        """ Abre o arquivo instructions.txt localmente no navegador padrão. """
        readme_path = os.path.join(os.path.dirname(__file__), "instructions.txt")
        if os.path.exists(readme_path):
            webbrowser.open("file://" + os.path.realpath(readme_path))
        else:
            messagebox.showerror(
                "Erro", "O arquivo instructions.txt não foi encontrado."
            )

    def open_config_window(self):
        """Abre a janela de configurações."""
        self.config_window = Toplevel(self.root)
        self.config_window.title("Configurações")
        self.config_window.configure(bg="#07171c")
        self.config_window.geometry("450x450")

        self.create_config_elements()

    def create_config_elements(self):
        """Cria elementos na janela de configuração para atualizar os seletores CSS e User-Agent."""
        self.config_frame = tk.Frame(self.config_window, bg="#07171c")
        self.config_frame.pack(pady=10)

        # Carrega as configurações atuais ou define os valores padrão
        config = self.load_current_config()

        # Campo para User-Agent
        self.user_agent_label = tk.Label(
            self.config_frame, text="User-Agent:", bg="#07171c", fg="white"
        )
        self.user_agent_label.pack(pady=5)
        self.user_agent_entry = tk.Entry(self.config_frame)
        self.user_agent_entry.insert(0, config.get("User-Agent", "Mozilla/5.0"))
        self.user_agent_entry.pack()

        # Campo para Cars Selector
        self.cars_selector_label = tk.Label(
            self.config_frame, text="Cars Selector:", bg="#07171c", fg="white"
        )
        self.cars_selector_label.pack(pady=5)
        self.cars_selector_entry = tk.Entry(self.config_frame)
        self.cars_selector_entry.insert(
            0, config.get("CarsSelector", "h1.e1ajxysh9.ooa-1ed90th.er34gjf0")
        )
        self.cars_selector_entry.pack()

        # Campo para Price Selector
        self.price_selector_label = tk.Label(
            self.config_frame, text="Price Selector:", bg="#07171c", fg="white"
        )
        self.price_selector_label.pack(pady=5)
        self.price_selector_entry = tk.Entry(self.config_frame)
        self.price_selector_entry.insert(
            0, config.get("PriceSelector", "h3.offer-price__number.eqdspoq4.ooa-o7wv9s.er34gjf0")
        )
        self.price_selector_entry.pack()

        # Campo para Others Selector
        self.others_selector_label = tk.Label(
            self.config_frame, text="Others Selector:", bg="#07171c", fg="white"
        )
        self.others_selector_label.pack(pady=5)
        self.others_selector_entry = tk.Entry(self.config_frame)
        self.others_selector_entry.insert(
            0, config.get("OthersSelector", "p.ezl3qpx3.ooa-1i4y99d.er34gjf0")
        )
        self.others_selector_entry.pack()

        # Campo para Brand Selector
        self.brand_selector_label = tk.Label(
            self.config_frame, text="Brand Selector:", bg="#07171c", fg="white"
        )
        self.brand_selector_label.pack(pady=5)
        self.brand_selector_entry = tk.Entry(self.config_frame)
        self.brand_selector_entry.insert(
            0,
            config.get(
                "BrandSelector", "h3.offer-title.big-text.ezl3qpx2.ooa-ebtemw.er34gjf0"
            ),
        )
        self.brand_selector_entry.pack()

        # Campo para URL Base
        self.base_url_label = tk.Label(
            self.config_frame, text="URL Base:", bg="#07171c", fg="white"
        )
        self.base_url_label.pack(pady=5)
        self.base_url_entry = tk.Entry(self.config_frame)
        self.base_url_entry.insert(
            0, config.get("BaseURL", "https://www.standvirtual.com/carros?page=")
        )
        self.base_url_entry.pack()

        # Botão para salvar as configurações
        self.save_config_button = tk.Button(
            self.config_frame,
            text="Salvar Configurações",
            command=self.save_config,
            bg="white",
            fg="black",
        )
        self.save_config_button.pack(pady=10)

    def load_current_config(self):
        """Carrega as configurações atuais do arquivo config.txt."""
        config = {}
        try:
            with open("config.txt", "r") as config_file:
                for line in config_file:
                    key, value = line.split(":", 1)
                    config[key.strip()] = value.strip()
        except FileNotFoundError:
            pass  # O arquivo config.txt não existe, usar valores padrão
        return config

    def save_config(self):
        """Salva as configurações alteradas no arquivo config.txt."""
        with open("config.txt", "w") as config_file:
            config_file.write(f"User-Agent:{self.user_agent_entry.get()}\n")
            config_file.write(f"CarsSelector:{self.cars_selector_entry.get()}\n")
            config_file.write(f"PriceSelector:{self.price_selector_entry.get()}\n")
            config_file.write(f"OthersSelector:{self.others_selector_entry.get()}\n")
            config_file.write(f"BrandSelector:{self.brand_selector_entry.get()}\n")
            config_file.write(f"BaseURL:{self.base_url_entry.get()}\n")
        messagebox.showinfo("Configurações", "Configurações salvas com sucesso!")

    def check_for_updates(self):
        current_version = "4.0.0"  # Versão atual do programa
        version_url = "https://raw.githubusercontent.com/pereira-andre/Scarpy/main/version.txt"

        try:
            response = requests.get(version_url)
            latest_version = response.text.strip()

            # Comparação de versões
            if latest_version < current_version:
                messagebox.showinfo(
                    "Programa Atualizado",
                    "A versão atual do programa é mais recente do que a disponível no site."
                )
            elif latest_version > current_version:
                messagebox.showinfo(
                    "Atualização Disponível",
                    f"Uma nova versão ({latest_version}) está disponível.\n"
                    "Por favor, visite o repositório do GitHub para atualizar."
                )
            else:
                messagebox.showinfo(
                    "Sem Atualizações", "Você está utilizando a versão mais recente."
                )
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
            "\n\nhttps://github.com/pereira-andre/Scarpy\nDez 2023"
        )
        messagebox.showinfo("Créditos", credits_text)

    def quit(self):
        """ Encerra o programa. """
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = MainGUI(root)
    root.mainloop()
