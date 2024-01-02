# scraping/html_fetcher.py

import os
import httpx
from selectolax.parser import HTMLParser


class HTMLFetcher:
    """
    Classe responsável por obter o HTML de páginas web.
    """

    def __init__(self):
        # Define o caminho para o arquivo de configuração
        config_path = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "config", "config.txt"
        )
        self.user_agent = self.load_user_agent(config_path)

    def load_user_agent(self, config_path):
        """
        Carrega o User-Agent do arquivo de configuração.
        """
        default_user_agent = "Mozilla/5.0"
        try:
            with open(config_path, "r") as config_file:
                for line in config_file:
                    if line.startswith("User-Agent:"):
                        return line.split(":", 1)[1].strip()
        except FileNotFoundError:
            print(
                f"Arquivo config.txt não encontrado em {config_path}. Usando User-Agent padrão."
            )
            return default_user_agent

    def get_html(self, url):
        """
        Obtém o HTML de uma URL.
        """
        headers = {"User-Agent": self.user_agent}
        try:
            response = httpx.get(url, headers=headers)
            response.raise_for_status()
            return HTMLParser(response.text)
        except Exception as e:
            print(f"Erro ao acessar {url}: {e}")
            return False
