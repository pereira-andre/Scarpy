import pandas as pd
import matplotlib.pyplot as plt

import pandas as pd
import matplotlib.pyplot as plt

def clean_data(csv_file):
    """Carrega e limpa os dados do arquivo CSV."""
    data = pd.read_csv(csv_file)
    # Limpa os dados removendo linhas com valores ausentes nas colunas especificadas
    clean_data = data.dropna(subset=['price', 'power', 'mileage', 'year', 'fuel'])
    return clean_data

def analyze_general_data(csv_file):
    """Gera estatísticas descritivas dos dados."""
    data = clean_data(csv_file)
    general_stats = data.describe()
    stats_str = general_stats.round(2).to_string()
    return stats_str


def analyze_data_and_save_figures(csv_file):
    """Analisa os dados do arquivo CSV e salva as figuras como imagens PNG."""
    data = pd.read_csv(csv_file)

    # Análise 1: Distribuição de Marcas
    fig = plot_brand_distribution(data)
    brand_distribution_path = 'brand_distribution.png'
    fig.savefig(brand_distribution_path)
    plt.close(fig)

    # Análise 2: Distribuição de Preços
    fig = plot_price_distribution(data)
    price_distribution_path = 'price_distribution.png'
    fig.savefig(price_distribution_path)
    plt.close(fig)

    return [brand_distribution_path, price_distribution_path]


def plot_brand_distribution(data):
    """Gera um gráfico da distribuição de marcas."""
    brand_counts = data['brand'].value_counts().head(10)
    fig, ax = plt.subplots(figsize=(10, 8))
    brand_counts.plot(kind='barh', ax=ax)
    ax.set(title='Top 10 Marcas Mais Comuns', xlabel='Frequência', ylabel='Marca')
    return fig


def plot_price_distribution(data):
    """Gera um gráfico da distribuição de preços."""
    fig, ax = plt.subplots(figsize=(10, 8))
    data['price'].plot(kind='hist', bins=30, ax=ax)
    ax.set(title='Distribuição dos Preços', xlabel='Preço', ylabel='Frequência')
    return fig



def analyze_max_min(csv_file):
    """Analisa o arquivo CSV para encontrar veículos específicos conforme critérios definidos."""
    data = clean_data(csv_file)

    # Encontrando veículos específicos
    most_expensive = data.loc[data['price'].idxmax()]
    cheapest = data.loc[data['price'].idxmin()]
    most_powerful = data.loc[data['power'].idxmax()]
    least_powerful = data.loc[data['power'].idxmin()]
    most_mileage = data.loc[data['mileage'].idxmax()]
    newest = data.loc[data['year'].idxmax()]
    oldest = data.loc[data['year'].idxmin()]

    # Construindo a string de resultado
    result_str = (
        f"Carro Mais Caro:\n{most_expensive}\n\n"
        f"Carro Mais Barato:\n{cheapest}\n\n"
        f"Carro Mais Potente:\n{most_powerful}\n\n"
        f"Carro Menos Potente:\n{least_powerful}\n\n"
        f"Carro com Mais Quilometragem:\n{most_mileage}\n\n"
        f"Carro Mais Recente:\n{newest}\n\n"
        f"Carro Mais Antigo:\n{oldest}\n"
    )

    return result_str

def save_fuel_type_distribution_figure(csv_file):
    """Gera e salva um gráfico da distribuição dos tipos de combustível."""
    data = pd.read_csv(csv_file)
    # Certifique-se de que 'fuel_type' é o nome correto da coluna no seu CSV.
    fuel_counts = data['fuel'].value_counts()
    fig, ax = plt.subplots(figsize=(10, 8))
    fuel_counts.plot(kind='bar', ax=ax)
    ax.set_title('Distribuição por Tipo de Combustível')
    ax.set_xlabel('Tipo de Combustível')
    ax.set_ylabel('Quantidade')
    plt.xticks(rotation=45)
    fig.tight_layout()
    # Salva o gráfico no mesmo diretório do script
    fig.savefig('fuel_type_distribution.png')
    plt.close(fig)
    return 'fuel_type_distribution.png'

def save_year_price_histogram(csv_file):
    data = pd.read_csv(csv_file)
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.hist(data['year'], bins=30, weights=data['price'], color='blue', edgecolor='black')
    ax.set_title('Relação Ano de Registro e Preço')
    ax.set_xlabel('Ano de Registro')
    ax.set_ylabel('Preço')
    fig.tight_layout()
    fig.savefig('year_price_histogram.png')
    plt.close(fig)
    return 'year_price_histogram.png'

def save_mileage_price_histogram(csv_file):
    data = pd.read_csv(csv_file)
    fig, ax = plt.subplots(figsize=(10, 8))
    ax.hist(data['mileage'], bins=30, weights=data['price'], color='green', edgecolor='black')
    ax.set_title('Relação Quilometragem e Preço')
    ax.set_xlabel('Quilometragem')
    ax.set_ylabel('Preço')
    fig.tight_layout()
    fig.savefig('mileage_price_histogram.png')
    plt.close(fig)
    return 'mileage_price_histogram.png'