# scraping/data_exporter.py

import csv
import json
import os
from pathlib import Path
from .car import Car


class DataExporter:
    """
    Classe responsável por exportar dados de automóveis para arquivos CSV e JSON.
    Esta classe fornece funcionalidades para guardar dados de automóveis em formatos
    de arquivo convenientes para análise e armazenamento de dados.
    """

    def __init__(self, filename="cars.csv"):
        """
        Inicializa o DataExporter com o nome do arquivo CSV.
        """
        # Define o caminho da pasta 'data_collected' relativo ao local deste arquivo
        base_dir = Path(__file__).parent.parent
        data_collected_dir = base_dir / "data_collected"

        # Cria a pasta 'data_collected' se ela não existir
        os.makedirs(data_collected_dir, exist_ok=True)

        # Define os caminhos para os arquivos CSV e JSON dentro da pasta 'data_collected'
        self.csv_filename = data_collected_dir / filename
        self.json_filename = self.csv_filename.with_suffix(".json")
        self.fieldnames = [
            "brand",
            "price",
            "fuel",
            "month",
            "year",
            "mileage",
            "power",
            "url",
        ]

        # Verifica se o arquivo CSV já existe; se não, cria um novo.
        if not self.csv_filename.exists():
            self.create_csv()

    def create_csv(self):
        """ Cria um novo arquivo CSV com os cabeçalhos apropriados. """
        with self.csv_filename.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()

    def __add__(self, other):
        """Sobrecarga do operador + para adicionar dados ao CSV."""
        if isinstance(other, (dict, Car)):
            self.append_to_csv(other)
        else:
            raise ValueError("Tipo de dados não suportado para exportação.")
        return self

    def append_to_csv(self, data):
        """
        Adiciona dados ao arquivo CSV. Aceita tanto dicionários quanto objetos Car.

        Args:
            data (dict or Car): Dados do automóvel para serem adicionados ao CSV.
        """
        if isinstance(data, dict):
            self._append_dict_to_csv(data)
        elif isinstance(data, Car):
            self._append_car_to_csv(data)
        else:
            raise ValueError("Tipo de dados não suportado para exportação.")

    def _append_dict_to_csv(self, car_data):
        """
        Adiciona um dicionário de dados de um automóvel ao arquivo CSV.

        Args:
            car_data (dict): Dicionário que contem os dados do automóvel.
        """
        with self.csv_filename.open("a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow(car_data)

    def _append_car_to_csv(self, car):
        """
        Adiciona dados de uma instância Car ao arquivo CSV.

        Args:
            car (Car): Objeto Car que contem os dados do automóvel.
        """
        car_data = {
            "brand": car.brand,
            "price": car.price,
            "fuel": car.fuel,
            "month": car.month,
            "year": car.year,
            "mileage": car.mileage,
            "power": car.power,
            "url": car.url,
        }
        self._append_dict_to_csv(car_data)

    def remove_duplicates(self):
        """
        Remove linhas duplicadas e linhas com dados insuficientes do arquivo CSV.
        """
        unique_data = set()
        rows = []
        with self.csv_filename.open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Verifica se a linha contém dados suficientes
                if sum(not cell.strip() for cell in row.values()) < len(row) - 1:
                    tuple_row = tuple(row.items())
                    # Adiciona a linha ao conjunto de dados únicos se ainda não estiver presente
                    if tuple_row not in unique_data:
                        unique_data.add(tuple_row)
                        rows.append(row)

        # Reescreve o arquivo CSV com as linhas únicas
        with self.csv_filename.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def convert_csv_to_json(self):
        """
        Converte os dados do arquivo CSV num arquivo JSON.
        Útil para aplicações que requerem manipulação de dados em formato JSON.
        """
        with self.csv_filename.open("r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            data = list(reader)

        # Escreve os dados no arquivo JSON
        with self.json_filename.open("w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
