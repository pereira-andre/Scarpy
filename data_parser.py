# data_parser.py

from urllib.parse import urljoin


class DataParser:
    """
    Classe DataParser responsável por analisar HTML e extrair informações específicas.

    Esta classe contém métodos para analisar páginas de busca e páginas individuais de itens,
    extraindo informações relevantes como detalhes do automóvel.
    """

    def parse_search_page(self, html):
        """
        Analisa a página de busca e extrai as URLs dos itens (automóveis).

        Args:
            html (HTMLParser): O objeto HTMLParser da página de busca.

        Yields:
            str: URLs dos automóveis encontrados na página de busca.
        """
        # Seleciona elementos HTML que correspondem a uma lista de automóveis na página de busca.
        cars = html.css("h1.ev7e6t89.ooa-1xvnx1e.er34gjf0")

        # Para cada automóvel encontrado, gera (yield) a URL completa do anúncio.
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
        # Extrai informações adicionais da página de um automóvel específico.
        others = self.extract_text(html, "p.e1aiyq9b1.ooa-1i4y99d.er34gjf0")

        # Separa e processa as informações como combustível, mês, ano, quilometragem e potência.
        fuel, month, year, mileage, power = self.parse_others(others)
        price_str = self.extract_text(
            html, "h3.offer-price__number.esicnpr5.ooa-17vk29r.er34gjf0"
        )
        price = self.parse_price(price_str)

        # Retorna um dicionário com todas as informações extraídas.
        return {
            "brand": self.extract_text(
                html, "h3.offer-title.big-text.e1aiyq9b2.ooa-ebtemw.er34gjf0"
            ),
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
