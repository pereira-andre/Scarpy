# data_parser.py

from urllib.parse import urljoin

class DataParser:
    """
    Classe DataParser responsável por analisar HTML e extrair informações específicas.

    Esta classe contém métodos para analisar páginas de busca e páginas individuais de itens,
    extraindo informações relevantes como detalhes do automóvel.
    """

    def __init__(self):
        # Defina os seletores padrão antes de tentar carregar do arquivo de configuração
        self.cars_selector = "h1.e1ajxysh9.ooa-1ed90th.er34gjf0"
        self.others_selector = "p.ezl3qpx3.ooa-1i4y99d.er34gjf0"
        self.brand_selector = "h3.offer-title.big-text.ezl3qpx2.ooa-ebtemw.er34gjf0"
        self.price_selector = "h3.offer-price__number.eqdspoq4.ooa-o7wv9s.er34gjf0"

        # Tente carregar os seletores personalizados do arquivo de configuração
        self.load_selectors()

    def load_selectors(self):
        """
        Carrega os seletores CSS a partir de um arquivo de configuração.
        """
        try:
            with open("config.txt", "r") as config_file:
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
            print("Arquivo de configuração não encontrado. Usando seletores padrão.")

    def set_default_selectors(self):
        """
        Define os seletores padrão para o caso de o arquivo de configuração não ser encontrado.
        """
        self.cars_selector = "h1.e1ajxysh9.ooa-1ed90th.er34gjf0"
        self.others_selector = "p.ezl3qpx3.ooa-1i4y99d.er34gjf0"
        self.brand_selector = "h3.offer-title.big-text.ezl3qpx2.ooa-ebtemw.er34gjf0"
        self.price_selector = "h3.offer-price__number.eqdspoq4.ooa-o7wv9s.er34gjf0"
        self.load_selectors()

    def parse_search_page(self, html):
        """
        Analisa a página de busca e extrai as URLs dos itens (automóveis).
        """
        cars = html.css(self.cars_selector)
        for car in cars:
            yield urljoin(
                "https://www.standvirtual.com/carros/anuncio",
                car.css_first("a").attributes["href"],
            )

    def parse_item_page(self, html):
        """
        Analisa a página de um item específico (automóvel) e extrai detalhes como marca, preço, etc.

        Args:
            html (HTMLParser): O objeto HTMLParser da página do item.

        Returns:
            dict: Um dicionário contendo informações extraídas sobre o automóvel.
        """
        others = self.extract_text(html, self.others_selector)
        fuel, month, year, mileage, power = self.parse_others(others)
        price_str = self.extract_text(html, self.price_selector)
        price = self.parse_price(price_str)

        return {
            "brand": self.extract_text(html, self.brand_selector),
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

        Args:
            html (HTMLParser): O objeto HTMLParser da página.
            selector (str): O seletor CSS para identificar o elemento desejado.

        Returns:
            str or None: O texto extraído do elemento, ou None se o elemento não for encontrado.
        """
        # Tenta extrair texto através de um seletor CSS específico. Retorna None se o elemento não for encontrado.
        try:
            return html.css_first(selector).text()
        except AttributeError:
            return None

    def parse_others(self, others_str):
        """
        Separa e processa informações adicionais do automóvel, como combustível, mês, ano, etc.

        Args:
            others_str (str): A string contendo as informações adicionais.

        Returns:
            tuple: Um tuple que contem combustível, mês, ano, quilometragem e potência.
        """
        # Separa a string com informações adicionais do automóvel e extrai cada parte.
        parts = others_str.split(" · ") if others_str else []
        # Inicializa as variáveis como None
        fuel, month, year, mileage, power = (None,) * 5

        if len(parts) > 0:
            fuel = parts[0]

        if len(parts) > 1:
            month = parts[1]

        if len(parts) > 2 and parts[2].isdigit():
            year = int(parts[2])

        if len(parts) > 3:
            mileage_str = parts[3].replace(" km", "").replace(" ", "")
            if mileage_str.isdigit():
                mileage = int(mileage_str)

        if len(parts) > 4:
            power_str = parts[4].replace(" cv", "").replace(" ", "")
            if power_str.isdigit():
                power = int(power_str)

        return fuel, month, year, mileage, power

    def parse_price(self, price_str):
        """
        Limpa e converte a string do preço para um valor numérico (float).

        Args:
            price_str (str): A string contendo o preço.

        Returns:
            float or None: O valor do preço convertido em float, ou None se não for possível converter.
        """
        if price_str:
            cleaned_price = (
                price_str.replace("€", "")
                .replace(" ", "")
                .replace(".", "")
                .replace(",", ".")
            )
            return float(cleaned_price)
        return None
