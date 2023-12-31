# Scarpy



# SCARPY - Automotive Data Collection & Analysis Application

SCARPY is an innovative application designed for collecting and analyzing automotive advertisement data from the Stand Virtual website. With a data-driven approach, SCARPY provides valuable insights and assists users in identifying the best vehicle deals.

## Features

- **Data Collection**: Gathers information from various pages of Stand Virtual, offering a comprehensive view of the automotive market.
- **Storage Formats**: Collected data is saved in `.csv` or `.json` formats, facilitating analysis and sharing.
- **Data Analysis**: Analyzes the collected data to identify market trends and discover unbeatable automotive offers.

## Prerequisites

To use SCARPY, Python must be installed. Additionally, some specific libraries are essential for the application's full functionality.

## Required Libraries

- `tkinter`: User interface.
- `pandas`: Data manipulation and analysis.
- `matplotlib`: Data visualization.
- `requests`: HTTP requests.
- `selectolax`: HTML parsing.
- `httpx`: Asynchronous HTTP requests.
- `threading`: Concurrent execution.

## Installation

Install the necessary libraries with the command:

```bash
pip install pandas matplotlib requests selectolax httpx
```

## Configuration

The application provides a configuration interface to adjust options such as:

- **Browser User-Agent**: Configure the User-Agent for HTTP requests, simulating your default browser. Go to Google, search for "my user agent," and copy and paste the result into SCARPY's settings for optimized browsing.
- **CSS Selectors**: Adapt the application to potential changes on the data source site.
- **Base URL**: Define the base URL of the site from where the data is collected.

## Execution

To run SCARPY, navigate to the application folder in the terminal and type:

```bash
python main.py
```

Configure the page range and pauses for data collection in the graphical interface.

## License

This project is licensed under the Apache 2.0 License. See the LICENSE file for more details.
