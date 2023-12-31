import os
from urllib.parse import urljoin


class DataParser:
    """
    Classe DataParser responsável por analisar HTML e extrair informações específicas,
    tais como detalhes do automóvel a partir de páginas de busca e páginas individuais de itens.
    """

    def __init__(self):
        # Constrói o caminho absoluto para o arquivo de configuração.
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "config", "config.txt"
        )
        self.load_selectors(config_path)

    def load_selectors(self, config_path):
        """
        Carrega os seletores CSS a partir de um arquivo de configuração.
        Se o arquivo não for encontrado, usa os seletores padrão.
        """
        try:
            with open(config_path, "r") as config_file:
                for line in config_file:
                    if line.startswith("CarsSelector:"):
                        self.cars_selector = line.split(":", 1)[1].strip()
                    elif line.startswith("OthersSelector:"):
                        self.others_selector = line.split(":", 1)[1].strip()
                    elif line.startswith("BrandSelector:"):
                        self.brand_selector = line.split(":", 1)[1].strip()
                    elif line.startswith("PriceSelector:"):
                        self.price_selector = line.split(":", 1)[1].strip()
        except FileNotFoundError:
            print(
                f"Arquivo de configuração não encontrado em {config_path}. Usando seletores padrão."
            )
            self.set_default_selectors()

    def set_default_selectors(self):
        """
        Define os seletores padrão para o caso de o arquivo de configuração não ser encontrado.
        """
        self.cars_selector = "h1.e1ajxysh9.ooa-1ed90th.er34gjf0"
        self.others_selector = "p.ezl3qpx3.ooa-1i4y99d.er34gjf0"
        self.brand_selector = "h3.offer-title.big-text.ezl3qpx2.ooa-ebtemw.er34gjf0"
        self.price_selector = "h3.offer-price__number.eqdspoq4.ooa-o7wv9s.er34gjf0"

    def parse_search_page(self, html):
        """
        Analisa a página de busca e extrai as URLs dos itens (automóveis).
        """
        cars = html.css(self.cars_selector)
        for car in cars:
            yield urljoin(
                "https://www.standvirtual.com", car.css_first("a").attributes["href"]
            )

    def parse_item_page(self, html):
        """
        Analisa a página de um item específico (automóvel) e extrai detalhes como marca, preço, etc.
        """
        brand = self.extract_text(html, self.brand_selector)
        price = self.parse_price(self.extract_text(html, self.price_selector))
        fuel, month, year, mileage, power = self.parse_others(
            self.extract_text(html, self.others_selector)
        )

        return {
            "brand": brand,
            "price": price,
            "fuel": fuel,
            "month": month,
            "year": year,
            "mileage": mileage,
            "power": power,
        }

    def extract_text(self, html, selector):
        """
        Extrai o texto de um elemento HTML usando um seletor CSS.
        """
        element = html.css_first(selector)
        return element.text().strip() if element else None

    def parse_others(self, others_str):
        """
        Separa e processa informações adicionais do automóvel.
        """
        parts = others_str.split(" · ") if others_str else []
        fuel, month, year, mileage, power = (None,) * 5

        if len(parts) >= 1:
            fuel = parts[0]
        if len(parts) >= 2:
            month = parts[1]
        if len(parts) >= 3:
            year = parts[2]
        if len(parts) >= 4:
            mileage = parts[3]
        if len(parts) >= 5:
            power = parts[4]

        return fuel, month, year, mileage, power

    def parse_price(self, price_str):
        """
        Limpa e converte a string do preço para um valor numérico (float).
        """
        if price_str:
            cleaned_price = (
                price_str.replace("€", "")
                .replace(" ", "")
                .replace(".", "")
                .replace(",", ".")
            )
            try:
                return float(cleaned_price)
            except ValueError:
                return None
        return None
