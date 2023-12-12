# Scarpy

## SCARPY - Automotive Data Collection & Analysis App

SCARPY is an application designed for collecting and analyzing automotive advertisement data from the Stand Virtual website.

### Features

- Collects data from a variety of Stand Virtual web pages.
- Stores data in .csv or .json formats.
- Analyzes the data to identify market trends and find the best automobile deals.

### Prerequisites

Before running the program, ensure you have Python installed on your operating system. Some libraries are required for the app to function correctly.

### Required Libraries

- `tkinter` - For the graphical user interface.
- `pandas` - For data manipulation and analysis.
- `matplotlib` - For data visualization.
- `requests` - For making HTTP requests.
- `selectolax` - For HTML parsing.
- `httpx` - For asynchronous HTTP requests.
- `threading` - For concurrent execution.

### Installation

To install the necessary libraries, execute the following command in your terminal:

```bash
pip install pandas matplotlib requests selectolax httpx
```

### Configuration

The app features a configuration window that allows you to easily adjust the following options:

- **Browser User-Agent**: To properly configure the User-Agent used in HTTP requests.
- **CSS Selectors**: To adapt the app to changes on the target website.
- **Base URL**: To define the base URL of the site from where the data is collected.

To access these configurations, run the app and click on the "Settings" button in the main menu.

### Execution

To run SCARPY, navigate to the app folder in your terminal and execute the command:

```bash
python main.py
```

### License

This project is licensed under the Apache 2.0 License - see the LICENSE file for more details.


This translated README maintains the structure and content of the original, ensuring clarity and coherence in English.
