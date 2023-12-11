#scraper_controller.py

import time
import random
from html_fetcher import HTMLFetcher
from data_parser import DataParser
from data_exporter import DataExporter


class ScraperController:
    """
    Classe que gere o processo de scraping de dados de automóveis.

    Combina as funcionalidades de HTMLFetcher, DataParser e DataExporter para recolher,
    analisar e exportar dados de automóveis de uma página web.
    """

    def __init__(self):
        self.html_fetcher = HTMLFetcher()
        self.data_parser = DataParser()
        self.data_exporter = DataExporter()
        self.interrupted = False

    def random_sleep(self, min_duration, max_duration):
        """
        Pausa a execução por um período aleatório entre min_duration e max_duration.
        Ajuda a evitar bloqueios ao fazer muitas requisições rápidas a um site.
        """
        time.sleep(random.uniform(min_duration, max_duration))

    def run(self, start_page=1, end_page=1, min_sleep=3, max_sleep=6):
        """
        Executa o processo de scraping, recolhendo dados de automóveis de várias páginas.
        """
        baseurl = "https://www.standvirtual.com/carros?page="
        self.status_message = ""

        try:
            for n in range(start_page, end_page + 1):
                if self.interrupted:
                    break
                print(f"Recolhendo página nº: {n}")

                page_url = baseurl + str(n)
                html = self.html_fetcher.get_html(page_url)
                if not html:
                    break

                cars_urls = self.data_parser.parse_search_page(html)
                for url in cars_urls:
                    if self.interrupted:
                        break
                    print(url)
                    html = self.html_fetcher.get_html(url)
                    car_data = self.data_parser.parse_item_page(html)
                    if car_data:
                        car_data["url"] = url
                        self.data_exporter.append_to_csv(car_data)
                        self.random_sleep(min_sleep, max_sleep)

            if self.interrupted:
                self.status_message = "Recolha cancelada pelo utilizador & dados guardados com sucesso."
            else:
                self.status_message = "Recolha concluída com sucesso."
        except Exception as e:
            self.status_message = f"Erro na recolha: {e}"

        finally:
            self.data_exporter.remove_duplicates()
            self.data_exporter.convert_csv_to_json()
            if self.interrupted:
                print("Recolha cancelada, dados guardados.")
            else:
                print("Recolha concluída, dados guardados.")
            return self.status_message

    def stop(self):
        """
        Interrompe o processo de scraping de forma segura.
        """
        self.interrupted = True
        self.data_exporter.remove_duplicates()
        self.data_exporter.convert_csv_to_json()
        print("Scraping interrompido - dados salvos.")
