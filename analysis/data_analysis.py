# data_analysis/data_analysis.py

import matplotlib

matplotlib.use("Agg")
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


    def generate_folder_name(self):
        """Gera o nome da pasta uma única vez."""
        current_time = datetime.now().strftime("%d-%m-%Y_%H-%M-%S")
        folder_name = f"{self.report_type}_Report_{current_time}"
        return folder_name

    def create_report_folder(self):
        """Cria a pasta do relatório com o nome gerado e retorna o caminho."""
        if self.report_folder_path is None:
            self.report_folder_name = self.generate_folder_name()
            self.report_folder_path = os.path.join(
                os.path.dirname(__file__), "..", "reports", self.report_folder_name
            )
            os.makedirs(self.report_folder_path, exist_ok=True)
        return self.report_folder_path

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
        for column in ["Preço", "Ano", "Quilometragem", "Potência"]:
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
            "price": "Preço",
            "year": "Ano",
            "mileage": "Quilometragem",
            "power": "Potência",
            "brand": "Marca",
            "fuel": "Combustível",
            "month": "Mês",
        }
        return data.rename(columns=colunas_em_portugues, inplace=False)

    def generate_visual_reports(self, filtered_data):
        plots_dir = os.path.join(self.report_folder_path, "plots")
        os.makedirs(plots_dir, exist_ok=True)

        graphs_paths = []

        # Gráfico 1: Distribuição de Preços por Tipo de Combustível
        plt.figure(figsize=(10, 6))
        ax = sns.boxplot(x="Combustível", y="Preço", data=filtered_data, palette="Set2")
        ax.set_title("Distribuição de Preços por Tipo de Combustível")
        graph_file_name = "preco_por_combustivel.png"
        plt.savefig(os.path.join(plots_dir, graph_file_name))
        graphs_paths.append(os.path.join("plots", graph_file_name))
        plt.close()

        # Gráfico 2: Quilometragem em Função do Ano de Fabricação
        plt.figure(figsize=(10, 6))
        ax = sns.scatterplot(
            x="Ano",
            y="Quilometragem",
            data=filtered_data,
            hue="Combustível",
            palette="coolwarm",
            s=100,
        )
        ax.set_title("Quilometragem em Função do Ano de Fabricação")
        ax.legend(title="Tipo de Combustível")
        graph_file_name = "quilometragem_por_ano.png"
        plt.savefig(os.path.join(plots_dir, graph_file_name))
        graphs_paths.append(os.path.join("plots", graph_file_name))
        plt.close()

        # Gráfico 3: Distribuição de Veículos por Tipo de Combustível
        plt.figure(figsize=(10, 6))
        ax = sns.countplot(x="Combustível", data=filtered_data, palette="viridis")
        ax.set_title("Distribuição de Veículos por Tipo de Combustível")
        ax.set_ylabel("Contagem")
        ax.set_xticklabels(ax.get_xticklabels(), rotation=45)
        graph_file_name = "distribuicao_por_combustivel.png"
        plt.savefig(os.path.join(plots_dir, graph_file_name))
        graphs_paths.append(os.path.join("plots", graph_file_name))
        plt.close()

        # Gráfico 4: Distribuição da Potência dos Veículos
        plt.figure(figsize=(10, 6))
        if not filtered_data["Potência"].empty:
            ax = sns.histplot(
                filtered_data["Potência"], kde=True, color="magenta", binwidth=20
            )
        ax.set_title("Distribuição da Potência dos Veículos")
        ax.set_xlabel("Potência (cv)")
        ax.set_ylabel("Contagem")
        graph_file_name = "distribuicao_potencia.png"
        plt.savefig(os.path.join(plots_dir, graph_file_name))
        graphs_paths.append(os.path.join("plots", graph_file_name))
        plt.close()

        # Gráfico 5: Distribuição de Veículos por Ano
        plt.figure(figsize=(10, 6))
        ax = sns.countplot(x="Ano", data=filtered_data, palette="viridis")
        ax.set_title("Contagem de Carros por Ano")
        ax.set_ylabel("Contagem")
        plt.xticks(rotation=45)
        graph_file_name = "contagem_por_ano.png"
        plt.savefig(os.path.join(plots_dir, graph_file_name))
        graphs_paths.append(os.path.join("plots", graph_file_name))
        plt.close()

        return graphs_paths

        print(f"Gráficos guardados em: {plots_dir}")


class StandardReportGenerator(ReportGeneratorBase):
    """
    Classe para gerar um relatório padrão.
    """

    def __init__(self, csv_file):
        super().__init__(csv_file, "Standard")
        self.report_folder_path = None

    def generate_html_report(self, filtered_data, report_title):
        report_folder_path = self.create_report_folder()  # Garante que a pasta do relatório é criada
        filtered_data = self.translate_columns(filtered_data)
        html_content = generate_html_header("Relatório de Análise Standard")

        graphs_paths = self.generate_visual_reports(filtered_data)

        # Sumário dos dados filtrados
        html_content += f"<div class='summary'><h2>Sumário do Relatório Standard</h2>"
        html_content += (
            f"<p>Total de Veículos Filtrados: {len(filtered_data)}</p></div>"
        )

        # Filtros Aplicados
        filters_text = ", ".join(
            [f"{key}: {value}" for key, value in self.filters_applied.items() if value]
        )
        html_content += f"<div class='filters-applied'><h2>Filtros Aplicados</h2><p>{filters_text}</p></div>"

        # Estatísticas Resumidas
        html_content += self.summarize_data(filtered_data)

        # Geradores de relatório:
        html_content += "<h2>Dados dos Veículos Filtrados</h2>"
        html_content += filtered_data.head(10).to_html(
            classes="dataframe", index=False, border=0, justify="left"
        )

        # Chamada para gerar os gráficos
        self.generate_visual_reports(filtered_data)

        # Inclusão dos gráficos
        html_content += "<h2>Gráficos Analíticos</h2>"
        for graph_path in graphs_paths:
            html_content += f"<img src='{graph_path}' style='width:100%; max-width:600px; height:auto; display:block; margin:20px auto;'>"

        # Salva o relatório HTML em pasta especifica
        report_file_path = os.path.join(report_folder_path, "report.html")
        with open(report_file_path, "w", encoding="utf-8") as file:
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
        return self.generate_html_report(filtered_data, "Relatório de Análise Standard")

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
        self.report_folder_path = None

    def generate_html_report(self, filtered_data, report_title):
        report_folder_path = self.create_report_folder()
        filtered_data = self.translate_columns(filtered_data)

        html_content = generate_html_header("Relatório de Análise Detalhada")

        graphs_paths = self.generate_visual_reports(filtered_data)

        # Cria o visualizador de distribuição de preços
        price_visualizer = PriceDistributionVisualizer(filtered_data)
        # Gera o gráfico de distribuição de preços dentro do diretório de plots do relatório
        price_distribution_graph_path = price_visualizer.generate_price_distribution_chart(
            report_folder_path + "/plots")
        graphs_paths.append(price_distribution_graph_path)

        # Sumário dos dados filtrados
        html_content += f"<div class='summary'><h2>Sumário do Relatório Detalhado</h2>"
        html_content += (
            f"<p>Total de Veículos Filtrados: {len(filtered_data)}</p></div>"
        )

        # Filtros Aplicados
        filters_text = ", ".join(
            [f"{key}: {value}" for key, value in self.filters_applied.items() if value]
        )
        html_content += f"<div class='filters-applied'><h2>Filtros Aplicados</h2><p>{filters_text}</p></div>"

        # Estatísticas Resumidas
        html_content += self.summarize_data(filtered_data)

        # Inclusão da tabela de dados filtrados
        html_content += "<h2>Dados dos Veículos Filtrados</h2>"
        html_content += filtered_data.to_html(
            classes="dataframe", index=False, border=0, justify="left"
        )

        # Inclusão dos gráficos
        html_content += "<h2>Gráficos Analíticos</h2>"
        for graph_path in graphs_paths:
            html_content += f"<img src='{graph_path}' style='width:100%; max-width:600px; height:auto; display:block; margin:20px auto;'>"

        # Salva o relatório HTML em pasta especifica
        report_file_path = os.path.join(report_folder_path, "report.html")
        with open(report_file_path, "w", encoding="utf-8") as file:
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
        return self.generate_html_report(filtered_data, "Relatório de Análise Detalhada")


    def generate_summary(self):
        # Gera um resumo para o relatório detalhado
        summary = "Sumário do Relatório Detalhado:\n"
        summary += f"Total de registos: {len(self.get_data())}\n"
        summary += "Detalhes adicionais: [inserir mais detalhes aqui]"
        return summary


# Funções Auxiliares
def generate_html_header(title):
    current_time = datetime.now().strftime("%H:%M %d/%m/%Y")
    logo_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "config", "assets", "logo.png"
    )
    css_styles = (
        "<style>"
        "body { font-family: Arial, sans-serif; margin: 0; padding: 0; }"
        "header { background-color: #07171c; color: white; padding: 10px 20px; display: flex; justify-content: space-between; align-items: center; }"
        ".logo { height: 50px; width: auto; }"  # Ajusta o tamanho do logo, mantendo a proporção
        ".title { flex-grow: 1; text-align: center; }"  # Centraliza o título
        ".date-time { text-align: right; }"  # Alinha a data e hora à direita
        ".header-section { display: flex; align-items: center; justify-content: center; }"  # Define o layout flexível para as seções do cabeçalho
        ".summary, .section { margin: 20px; }"
        "h2 { color: #333; }"
        "table { width: 100%; border-collapse: collapse; margin-top: 20px; }"
        "th, td { text-align: left; padding: 8px; border-bottom: 1px solid #ddd; }"
        "th { background-color: #f2f2f2; }"
        "</style>"
    )
    header_html = (
        f"<header>"
        f"<div class='header-section'><img src='file://{logo_path}' class='logo'/></div>"
        f"<div class='header-section title'><h1>{title}</h1></div>"
        f"<div class='header-section date-time'><p>{current_time}</p></div>"
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


class PriceDistributionVisualizer:
    def __init__(self, data):
        self.data = data

    def generate_price_distribution_chart(self, output_dir):
        plots_dir = output_dir  # Use diretamente o output_dir
        os.makedirs(plots_dir, exist_ok=True)

        graph_file_name = "price_distribution.png"
        graph_path = os.path.join(plots_dir, graph_file_name)

        plt.figure(figsize=(10, 6))
        sns.histplot(self.data['Preço'], kde=True)
        plt.title('Distribuição de Preços dos Veículos')
        plt.xlabel('Preço')
        plt.ylabel('Frequência')
        plt.savefig(graph_path)
        plt.close()

        return graph_path



