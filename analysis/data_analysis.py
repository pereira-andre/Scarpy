# data_analysis/data_analysis.py

import pandas as pd
import os
from abc import ABC
from datetime import datetime


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


class StandardReportGenerator(ReportGeneratorBase):
    """
    Classe para gerar um relatório padrão.
    """

    def __init__(self, csv_file):
        super().__init__(csv_file, "Standard")

    def generate_html_report(self, filtered_data):
        # Gera um relatório HTML padrão
        html_content = generate_html_header("Relatório de Análise Standard")
        html_content += f"<div class='summary'>{self.generate_summary()}</div>"

        # Incluir filtros aplicados
        filters_text = ", ".join(
            [f"{key}: {value}" for key, value in self.filters_applied.items() if value]
        )
        html_content += f"<p>Filtros Aplicados: {filters_text}</p>"

        html_content += generate_statistics_summary(filtered_data)
        html_content += filtered_data.head(10).to_html(index=False)
        report_file_path = os.path.join(
            os.path.dirname(__file__), "..", "reports", "standard_report.html"
        )
        with open(report_file_path, "w") as file:
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
        # Gera um resumo para o relatório padrão
        summary = "Sumário do Relatório Standard:\n"
        summary += f"Total de registos: {len(self.get_data())}\n"
        return summary


class DetailedReportGenerator(ReportGeneratorBase):
    """
    Classe para gerar um relatório detalhado.
    """

    def __init__(self, csv_file):
        super().__init__(csv_file, "Detailed")

    def generate_html_report(self, filtered_data):
        # Gera um relatório HTML detalhado
        html_content = generate_html_header("Relatório de Análise Completo")
        html_content += f"<div class='summary'>{self.generate_summary()}</div>"

        # Incluir filtros aplicados
        filters_text = ", ".join(
            [f"{key}: {value}" for key, value in self.filters_applied.items() if value]
        )
        html_content += f"<p>Filtros Aplicados: {filters_text}</p>"

        html_content += generate_statistics_summary(filtered_data)
        html_content += filtered_data.describe().to_html()
        html_content += filtered_data.to_html(index=False)
        report_file_path = os.path.join(
            os.path.dirname(__file__), "..", "reports", "detailed_report.html"
        )
        with open(report_file_path, "w") as file:
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


# Funções Auxiliares
def generate_html_header(title):
    # Constrói o caminho absoluto para o logo
    logo_path = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), "config", "assets", "logo.png"
    )

    # Estilos CSS
    css_styles = (
        "<style>"
        "header { display: flex; justify-content: space-between; align-items: center; }"
        "h1 { text-align: center; }"
        ".logo { width: 100px; height: 100px; }"
        ".header-right { text-align: right; }"
        "</style>"
    )

    # Cabeçalho HTML
    header_html = (
        f"<header>"
        f"<div></div>"  # Espaço vazio para alinhamento
        f"<h1>{title}</h1>"
        f"<div class='header-right'>"
        f"<img src='file://{logo_path}' class='logo'/>"  # Referência ao logo
        f"<p>{datetime.now().strftime('%d/%m/%Y %H:%M')}</p>"
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
