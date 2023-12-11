import csv
import json
from pathlib import Path


class DataExporter:
    """
    Classe DataExporter responsável por exportar os dados extraídos para diferentes formatos.

    Esta classe cria e manipula arquivos CSV e JSON.
    """

    def __init__(self, filename="cars.csv"):
        """
        Inicializa o nome do arquivo CSV e cria o arquivo com cabeçalhos, se ainda não existir.

        Args:
            filename (str): Nome do arquivo CSV a ser criado ou manipulado.
        """
        self.csv_filename = Path(filename)
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
        if not self.csv_filename.exists():
            self.create_csv()

    def create_csv(self):
        """
        Cria o arquivo CSV com os cabeçalhos apropriados.
        """
        with self.csv_filename.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()

    def append_to_csv(self, car_data):
        """
        Adiciona um anúnico ao arquivo CSV.

        Args:
            car_data (dict): Dicionário que contém os dados do automóvel a ser adicionado.
        """
        with self.csv_filename.open("a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow(car_data)

    def remove_duplicates(self):
        """
        Remove linhas duplicadas do arquivo CSV.

        Este método lê o arquivo CSV, remove registos duplicados e reescreve o arquivo.
        """
        unique_data = set()
        rows = []
        with self.csv_filename.open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                tuple_row = tuple(row.items())
                if tuple_row not in unique_data:
                    unique_data.add(tuple_row)
                    rows.append(row)

        with self.csv_filename.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def convert_csv_to_json(self):
        """
        Converte os dados do arquivo CSV para um formato JSON.

        Este método lê o arquivo CSV e grava os dados num arquivo JSON.
        """
        with self.csv_filename.open("r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            data = list(reader)

        with self.json_filename.open("w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
