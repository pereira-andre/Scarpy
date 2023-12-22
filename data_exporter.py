import csv
import json
from pathlib import Path
from car import Car

class DataExporter:
    """
    Classe responsável por exportar dados de automóveis para arquivos CSV e JSON.
    """

    def __init__(self, filename="cars.csv"):
        """
        Inicializa o DataExporter com o nome do arquivo CSV.

        Args:
            filename (str): Nome do arquivo CSV para exportação.
        """
        self.csv_filename = Path(filename)
        self.json_filename = self.csv_filename.with_suffix(".json")
        self.fieldnames = [
            "brand", "price", "fuel", "month", "year", "mileage", "power", "url"
        ]
        if not self.csv_filename.exists():
            self.create_csv()

    def create_csv(self):
        """ Cria um novo arquivo CSV com cabeçalhos apropriados. """
        with self.csv_filename.open("w", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writeheader()

    def append_to_csv(self, data):
        """
        Sobrecarrega o método append_to_csv para aceitar diferentes tipos de dados.

        Args:
            data (dict or Car): Dados do automóvel, que podem ser um dicionário ou um objeto Car.
        """
        if isinstance(data, dict):
            self._append_dict_to_csv(data)
        elif isinstance(data, Car):
            self._append_car_to_csv(data)
        else:
            raise ValueError("Tipo de dado não suportado para exportação.")

    def _append_dict_to_csv(self, car_data):
        """
        Adiciona um dicionário ao arquivo CSV.

        Args:
            car_data (dict): Dicionário contendo dados do automóvel.
        """
        with self.csv_filename.open("a", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=self.fieldnames)
            writer.writerow(car_data)

    def _append_car_to_csv(self, car):
        """
        Adiciona dados de uma instância Car ao arquivo CSV.

        Args:
            car (Car): Objeto Car contendo dados do automóvel.
        """
        car_data = {
            "brand": car.brand,
            "price": car.price,
            "fuel": car.fuel,
            "month": car.month,
            "year": car.year,
            "mileage": car.mileage,
            "power": car.power,
            "url": car.url
        }
        self._append_dict_to_csv(car_data)

    def remove_duplicates(self):
        """ Remove linhas duplicadas e linhas com dados insuficientes do arquivo CSV. """
        unique_data = set()
        rows = []
        with self.csv_filename.open("r", newline="", encoding="utf-8") as file:
            reader = csv.DictReader(file)
            for row in reader:
                # Verifica se a maioria dos campos está vazia
                if sum(not cell.strip() for cell in row.values()) < len(row) - 1:
                    tuple_row = tuple(row.items())
                    if tuple_row not in unique_data:
                        unique_data.add(tuple_row)
                        rows.append(row)

        with self.csv_filename.open("w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=self.fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def convert_csv_to_json(self):
        """ Converte os dados do arquivo CSV em um arquivo JSON. """
        with self.csv_filename.open("r", encoding="utf-8") as csv_file:
            reader = csv.DictReader(csv_file)
            data = list(reader)

        with self.json_filename.open("w", encoding="utf-8") as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
