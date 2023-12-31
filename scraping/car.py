# scraping/car.py


class Car:
    """
    Classe Car representa um automóvel com várias características.

    Atributos:
        brand (str): Marca do automóvel.
        price (float): Preço do automóvel.
        fuel (str): Tipo de combustível do automóvel.
        month (str): Mês de fabricação do automóvel.
        year (int): Ano de fabricação do automóvel.
        mileage (int): Quilometragem do automóvel.
        power (int): Potência do automóvel em cavalos.
        url (str): URL do anúncio do automóvel.
    """

    def __init__(
        self,
        brand=None,
        price=None,
        fuel=None,
        month=None,
        year=None,
        mileage=None,
        power=None,
        url=None,
    ):
        self.brand = brand
        self.price = price
        self.fuel = fuel
        self.month = month
        self.year = year
        self.mileage = mileage
        self.power = power
        self.url = url

    def __str__(self):
        return f"Car(brand={self.brand}, price={self.price}, fuel={self.fuel}, month={self.month}, year={self.year}, mileage={self.mileage}, power={self.power}, url={self.url})"
