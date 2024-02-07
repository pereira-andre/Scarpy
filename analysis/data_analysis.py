# data_analysis/data_analysis.py

import matplotlib
matplotlib.use('Agg')  # Define o backend antes de importar pyplot
import matplotlib.pyplot as plt

import pandas as pd
import os
from abc import ABC
from datetime import datetime
import seaborn as sns

class DataAnalysisBase(ABC):
    """
    Classe base abstrata para análise de dados. Define uma estrutura comum e métodos para análise de dados.
    """

    def __init__(self, csv_file):
        # Carrega dados do arquivo CSV e limpa os dados
        self.__data = pd.read_csv(csv_file)
        self.clean_data()

    def clean_data(self):
        # Remove valores nulos dos dados
        self.__data.dropna(inplace=True)

    def get_data(self):
        # Retorna os dados
        return self.__data

    def set_data(self, new_data):
        # Define novos dados se forem um DataFrame
        if isinstance(new_data, pd.DataFrame):
            self.__data = new_data
        else:
            raise ValueError("Os dados devem ser um DataFrame")

    def add_data(self, data, replace=False, csv_path=None):
        # Carrega dados de um arquivo CSV, se fornecido, e adiciona os dados existentes
        if csv_path:
            try:
                new_data = pd.read_csv(csv_path)
            except FileNotFoundError:
                raise ValueError("Caminho do arquivo inválido.")
        elif isinstance(data, pd.DataFrame):
            new_data = data
        else:
            raise TypeError(
                "data deve ser um DataFrame ou None se csv_path for fornecido."
            )
        if replace:
            self.__data = new_data
        else:
            self.__data = pd.concat([self.__data, new_data])

    def filter_data(self, **kwargs):
        # Filtra os dados com base em critérios fornecidos
        filtered_data = self.get_data()
        for key, value in kwargs.items():
            if value:
                if key in ["min_price", "min_mileage", "min_power", "min_year"]:
                    column_name = key.split("_")[1]
                    filtered_data = filtered_data[filtered_data[column_name] >= value]
                elif key in ["max_price", "max_mileage", "max_power", "max_year"]:
                    column_name = key.split("_")[1]
                    filtered_data = filtered_data[filtered_data[column_name] <= value]
                elif key == "brand":
                    filtered_data = filtered_data[
                        filtered_data["brand"].str.contains(value, case=False, na=False)
                    ]
                elif key in ["fuel", "month"]:
                    filtered_data = filtered_data[filtered_data[key] == value]
        return filtered_data

    def generate_report(self, **kwargs):
        # Método abstrato para gerar o relatório
        raise NotImplementedError(
            "Método abstrato deve ser implementado nas subclasses."
        )

    def generate_summary(self):
        # Método abstrato para gerar o resumo
        raise NotImplementedError(
            "Método abstrato deve ser implementado nas subclasses."
        )


class ReportGeneratorBase(DataAnalysisBase):
    """
    Classe intermédia para gerar relatórios. Herda de DataAnalysisBase.
    """

    def __init__(self, csv_file, report_type):
        super().__init__(csv_file)
        self.report_type = report_type
        self.filters_applied = None

    def __str__(self):
        # Representação em string da instância
        return f"Report Type: {self.report_type}"

    def generate_report(self, **kwargs):
        # Método abstrato para gerar o relatório
        raise NotImplementedError(
            "Método abstrato deve ser implementado nas subclasses."
        )

    def summarize_data(self, filtered_data):
        summary_stats = filtered_data.describe().round(2)
        stats_html = "<div class='statistics-summary'><h2>Estatísticas Resumidas</h2>"
        for column in ['Preço', 'Ano', 'Quilometragem', 'Potência']:
            stats_html += (
                f"<p><strong>{column}:</strong><br>"
                f"Média: {summary_stats.at['mean', column]}, "
                f"Mínimo: {summary_stats.at['min', column]}, "
                f"Máximo: {summary_stats.at['max', column]}, "
                f"Desvio padrão: {summary_stats.at['std', column]}</p>"
            )
        stats_html += "</div>"
        return stats_html

    def translate_columns(self, data):
        colunas_em_portugues = {
            'price': 'Preço',
            'year': 'Ano',
            'mileage': 'Quilometragem',
            'power': 'Potência',
            'brand': 'Marca',
            'fuel': 'Combustível',
            'month': 'Mês',
            # Adicione mais mapeamentos conforme necessário
        }
        return data.rename(columns=colunas_em_portugues, inplace=False)


class StandardReportGenerator(ReportGeneratorBase):
    """
    Classe para gerar um relatório padrão.
    """

    def __init__(self, csv_file):
        super().__init__(csv_file, "Standard")

    def generate_html_report(self, filtered_data):
        filtered_data = self.translate_columns(filtered_data)
        html_content = generate_html_header("Relatório de Análise Standard")

        # Sumário dos dados filtrados
        html_content += f"<div class='summary'><h2>Sumário do Relatório Standard</h2>"
        html_content += f"<p>Total de Veículos Filtrados: {len(filtered_data)}</p></div>"

        # Filtros Aplicados - Agora antes das Estatísticas Resumidas
        filters_text = ", ".join([f"{key}: {value}" for key, value in self.filters_applied.items() if value])
        html_content += f"<div class='filters-applied'><h2>Filtros Aplicados</h2><p>{filters_text}</p></div>"

        # Estatísticas Resumidas
        html_content += self.summarize_data(filtered_data)

        # Após a seção de filtros aplicados em ambos os geradores de relatório:
        html_content += "<h2>Dados dos Veículos Filtrados</h2>"
        html_content += filtered_data.head(10).to_html(classes='dataframe', index=False, border=0, justify='left')

        # Salva o relatório HTML
        report_file_path = os.path.join(os.path.dirname(__file__), "..", "reports", "standard_report.html")
        with open(report_file_path, "w", encoding='utf-8') as file:
            file.write(html_content)
        print(f"Relatório salvo em: {report_file_path}")
        return report_file_path

    def generate_report(self, data=None, **kwargs):
        # Armazena os filtros aplicados e gera o relatório
        self.filters_applied = kwargs
        if data is None:
            filtered_data = self.filter_data(**kwargs)
        else:
            filtered_data = data
        return self.generate_html_report(filtered_data)

    def generate_summary(self):
        # Gera um resumo para o relatório padrão
        summary = "Sumário do Relatório Standard:\n"
        summary += f"Total de registros: {len(self.get_data())}\n"
        return summary


class DetailedReportGenerator(ReportGeneratorBase):
    """
    Classe para gerar um relatório detalhado.
    """

    def __init__(self, csv_file):
        super().__init__(csv_file, "Detailed")

    def generate_html_report(self, filtered_data):
        filtered_data = self.translate_columns(filtered_data)
        html_content = generate_html_header("Relatório de Análise Detalhada")

        # Sumário dos dados filtrados
        html_content += f"<div class='summary'><h2>Sumário do Relatório Detalhado</h2>"
        html_content += f"<p>Total de Veículos Filtrados: {len(filtered_data)}</p></div>"

        # Filtros Aplicados - Agora antes das Estatísticas Resumidas
        filters_text = ", ".join([f"{key}: {value}" for key, value in self.filters_applied.items() if value])
        html_content += f"<div class='filters-applied'><h2>Filtros Aplicados</h2><p>{filters_text}</p></div>"

        # Estatísticas Resumidas
        html_content += self.summarize_data(filtered_data)

        # Inclusão da tabela de dados filtrados
        html_content += "<h2>Dados dos Veículos Filtrados</h2>"
        html_content += filtered_data.to_html(classes='dataframe', index=False, border=0, justify='left')

        # Geração dos gráficos
        self.generate_visual_reports(filtered_data)

        # Inclusão dos gráficos
        html_content += "<h2>Gráficos Analíticos</h2>"
        graphs = ["preco_por_combustivel.png", "quilometragem_por_ano.png", "distribuicao_por_combustivel.png",
                  "distribuicao_potencia.png"]
        for graph in graphs:
            html_content += f"<img src='../reports/plots/{graph}' style='width:100%; max-width:600px; height:auto; display:block; margin:20px auto;'>"

        # Salva o relatório HTML
        report_file_path = os.path.join(os.path.dirname(__file__), "..", "reports", "detailed_report.html")
        with open(report_file_path, "w", encoding='utf-8') as file:
            file.write(html_content)

        return report_file_path

    def generate_report(self, data=None, **kwargs):
        # Armazena os filtros aplicados e gera o relatório
        self.filters_applied = kwargs
        if data is None:
            filtered_data = self.filter_data(**kwargs)
        else:
            filtered_data = data
        return self.generate_html_report(filtered_data)

    def generate_summary(self):
        # Gera um resumo para o relatório detalhado
        summary = "Sumário do Relatório Detalhado:\n"
        summary += f"Total de registos: {len(self.get_data())}\n"
        summary += "Detalhes adicionais: [inserir mais detalhes aqui]"
        return summary

    def generate_visual_reports(self, filtered_data):
        """
        Gera gráficos visuais para o relatório com base nos dados filtrados.
        """
        sns.set(style="whitegrid")  # Configuração do estilo do Seaborn

        # Diretório para salvar os gráficos
        plots_dir = os.path.join(os.path.dirname(__file__), "..", "reports", "plots")
        os.makedirs(plots_dir, exist_ok=True)  # Cria o diretório se não existir

        # Gráfico 1: Distribuição de Preços por Tipo de Combustível
        plt.figure(figsize=(10, 6))
        ax = sns.boxplot(x='Combustível', y='Preço', data=filtered_data, palette='Set2')
        ax.set_title('Distribuição de Preços por Tipo de Combustível')
        plt.savefig(os.path.join(plots_dir, 'preco_por_combustivel.png'))
        plt.close()

        # Gráfico 2: Quilometragem em Função do Ano de Fabricação
        plt.figure(figsize=(10, 6))
        ax = sns.scatterplot(x='Ano', y='Quilometragem', data=filtered_data, hue='Combustível', palette='coolwarm',
                             s=100)
        ax.set_title('Quilometragem em Função do Ano de Fabricação')
        ax.legend(title='Tipo de Combustível')
        plt.savefig(os.path.join(plots_dir, 'quilometragem_por_ano.png'))
        plt.close()

        # Gráfico 3: Distribuição de Veículos por Tipo de Combustível
        plt.figure(figsize=(10, 6))
        ax = sns.countplot(x='Combustível', data=filtered_data, palette='viridis')
        ax.set_title('Distribuição de Veículos por Tipo de Combustível')
        ax.set_ylabel('Contagem')  # Altera a etiqueta do eixo y para 'Contagem'
        ax.set_xticklabels(ax.get_xticklabels(), rotation=0)  # Ajusta para horizontal
        plt.savefig(os.path.join(plots_dir, 'distribuicao_por_combustivel.png'))
        plt.close()

        # Gráfico 4: Distribuição da Potência dos Veículos
        plt.figure(figsize=(10, 6))
        ax = sns.histplot(filtered_data['Potência'], kde=True, color='magenta', binwidth=20)
        ax.set_title('Distribuição da Potência dos Veículos')
        ax.set_xlabel('Potência (cv)')
        ax.set_ylabel('Contagem')  # Altera a etiqueta do eixo y para 'Contagem'
        plt.savefig(os.path.join(plots_dir, 'distribuicao_potencia.png'))
        plt.close()

        print(f"Gráficos salvos em: {plots_dir}")


# Funções Auxiliares
def generate_html_header(title):
    logo_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "config", "assets", "logo.png"
    )
    css_styles = (
        "<style>"
        "body { font-family: Arial, sans-serif; margin: 0; padding: 0; }"
        "header { background-color: #07171c; color: white; padding: 10px 20px; display: flex; justify-content: space-between; align-items: center; }"
        "h1 { margin: 0; }"
        ".logo { height: 50px; }"
        ".summary, .section { margin: 20px; }"
        "h2 { color: #333; }"
        "table { width: 100%; border-collapse: collapse; margin-top: 20px; }"
        "th, td { text-align: left; padding: 8px; border-bottom: 1px solid #ddd; }"
        "th { background-color: #f2f2f2; }"
        "img { width: 100%; max-width: 600px; height: auto; display: block; margin: 20px auto; }"
        ".statistics-summary p, .filters-applied { margin: 10px 0; }"
        "</style>"
    )
    header_html = (
        f"<header>"
        f"<h1>{title}</h1>"
        f"<div class='header-right'>"
        f"<img src='file://{logo_path}' class='logo'/>"
        f"</div>"
        f"</header>"
    )
    return css_styles + header_html


def generate_statistics_summary(dataframe):
    # Função para gerar um resumo das estatísticas descritivas
    description = dataframe.describe()
    relevant_stats = description.loc[["mean", "min", "max", "std"]]
    html_content = ""
    for col in relevant_stats.columns:
        html_content += (
            f"<p><strong>{col.title()}:</strong><br>"
            f"Média: {relevant_stats.at['mean', col]:.2f}, "
            f"Mínimo: {relevant_stats.at['min', col]}, "
            f"Máximo: {relevant_stats.at['max', col]}, "
            f"Desvio padrão: {relevant_stats.at['std', col]:.2f}</p>"
        )
    return html_content

