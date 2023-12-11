# Scarpy

## SCARPY - Automotive Data Collection & Analysis App

SCARPY is an application designed for collecting and analyzing automotive advertisement data from the Stand Virtual website.

### Features

- Collect data from a range of web pages on Stand Virtual.
- Store the collected data in .csv or .json formats.
- Analyze the data to identify market trends and find the best automobile deals.

### Prerequisites

Before running the program, ensure you have Python installed on your system. You will also need several libraries for the application to function correctly.

### Required Libraries

- `tkinter` - For the graphical user interface.
- `pandas` - For data manipulation and analysis.
- `matplotlib` - For data visualization.
- `requests` - For making HTTP requests.
- `selectolax` - For HTML parsing.
- `httpx` - For asynchronous HTTP requests.
- `threading` - For concurrent execution.

### Installation

To install the required libraries, run the following command in your terminal:

```bash
pip install pandas matplotlib requests selectolax httpx
```

### Configuring the Browser

To ensure the application fetches data correctly, it is necessary to configure the browser's User-Agent in the `html_fetcher.py` file. Follow these steps:

1. Open your web browser and search for "my user agent".
2. Copy the User-Agent string displayed.
3. In the `html_fetcher.py` file, find the `headers` variable and replace the existing User-Agent value with your copied string. 

   For example:

   ```python
   headers = {
       "User-Agent": "Your User-Agent String Here"
   }
   ```

### Running the Application

To run SCARPY, navigate to the application directory in your terminal and execute:

```bash
python main.py
```

### License

This project is licensed under the Apache 2.0 License - see the LICENSE file for details.
