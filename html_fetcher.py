#html_fetcher.py

import httpx
from selectolax.parser import HTMLParser

class HTMLFetcher:
    """
    Classe responsável por procurar o HTML de páginas web.
    """

    def get_html(self, url):
        """
        Obtém o HTML de uma página web a partir da URL fornecida.

        Args:
            url (str): A URL da página.

        Returns:
            HTMLParser: Objeto HTMLParser que contém o HTML da página, ou False se a requisição falhar.
        """
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }

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
