#html_fetcher.py

import httpx
from selectolax.parser import HTMLParser

class HTMLFetcher:
    """
    Classe responsável por procurar o HTML de páginas web.
    """

    @staticmethod
    def get_html(url):
        """
        Obtém o HTML de uma página web a partir da URL fornecida.

        Args:
            url (str): A URL da página.

        Returns:
            HTMLParser: Objeto HTMLParser que contém o HTML da página, ou False se a requisição falhar.
        """
        user_agent = "Mozilla/5.0"  # Valor padrão

        # Tente ler o User-Agent do arquivo de configurações
        try:
            with open("config.txt", "r") as config_file:
                for line in config_file:
                    if line.startswith("User-Agent:"):
                        user_agent = line.split(":", 1)[1].strip()
                        break
        except FileNotFoundError:
            print("Arquivo config.txt não encontrado. Usando User-Agent padrão.")

        headers = {"User-Agent": user_agent}

        # Tente fazer a requisição HTTP
        try:
            response = httpx.get(url, headers=headers, follow_redirects=True)
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            print(f"Erro HTTP {exc.response.status_code} ao solicitar {exc.request.url!r}.")
            return False
        except httpx.ReadTimeout as exc:
            print(f"Timeout ao acessar {exc.request.url!r}.")
            return False
        except httpx.RequestError as exc:
            print(f"Erro ao fazer a requisição para {exc.request.url!r}: {exc}")
            return False

        return HTMLParser(response.text)
