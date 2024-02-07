# SCARPY - Aplicação de Recolha e Análise de Dados Automóveis

SCARPY é uma aplicação inovadora concebida para recolher e analisar dados de anúncios de automóveis do site Stand Virtual. Com uma abordagem orientada para os dados, SCARPY oferece percepções valiosas e auxilia os utilizadores a identificar as melhores ofertas de veículos.

## Funcionalidades

- **Recolha de Dados**: Obtém informações de várias páginas do Stand Virtual, proporcionando uma visão abrangente do mercado automóvel.
- **Formatos de Armazenamento**: Os dados recolhidos são guardados em formatos `.csv` ou `.json`, facilitando a análise e partilha.
- **Análise de Dados**: Analisa os dados recolhidos para identificar tendências de mercado e descobrir ofertas automóveis imperdíveis.

## Pré-requisitos

Para utilizar o SCARPY, é necessário ter instalado o Python. Adicionalmente, algumas bibliotecas específicas são fundamentais para o funcionamento completo da aplicação.

## Bibliotecas Necessárias

- `tkinter`: Interface gráfica do utilizador.
- `pandas`: Manipulação e análise de dados.
- `seaborn`: Visualização de dados estatística baseada no matplotlib.
- `matplotlib`: Visualização de dados.
- `requests`: Realização de solicitações HTTP.
- `selectolax`: Análise de HTML.
- `httpx`: Solicitações HTTP assíncronas.
- `threading`: Execução concorrente.

## Instalação

Instale as bibliotecas necessárias com o comando:

```bash
pip install pandas matplotlib seaborn requests selectolax httpx
```

## Configuração

A aplicação oferece uma interface de configurações para ajustar opções como:

- **User-Agent do Navegador**: Configure o User-Agent para solicitações HTTP, simulando o seu navegador padrão. Aceda ao Google, pesquise por "my user agent" e copie e cole o resultado nas configurações do SCARPY para uma navegação otimizada.
- **Seletores CSS**: Adapte a aplicação a eventuais mudanças no site de origem dos dados.
- **URL Base**: Defina a URL base do site de onde os dados são recolhidos.

## Execução

Para executar o SCARPY, aceda à pasta da aplicação no terminal e digite:

```bash
python main.py
```

Configure o intervalo de páginas e as pausas para a recolha de dados na interface gráfica.

## Licença

Este projeto é licenciado sob a Licença Apache 2.0. Consulte o arquivo LICENSE para obter mais detalhes.