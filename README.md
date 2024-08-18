# Stock Analyzer

A Python-based stock analysis application that fetches stock data and news stories, plots the stock prices, and displays related news articles. The application features interactive graphing, news article display, and is designed with a portrait-oriented GUI.

## Features

- **Stock Data Visualization**: Plots the closing prices of stocks over a user-defined date range with interactive hover information.
- **News Aggregation**: Fetches and displays news articles related to the stock ticker.
- **Resizable Graph**: Allows users to resize the plot according to their preference.
- **Scrollable News Frame**: Provides a scrollable area to view multiple news articles.

## Requirements

- Python 3.x
- `yfinance` for fetching stock data
- `matplotlib` for plotting
- `PIL` (Pillow) for image handling
- `requests` for API requests
- `mplcursors` for interactive hover functionality
- News API key for fetching news articles (sign up at [NewsAPI](https://newsapi.org/) to get your key)


## Usage

1. **Run the Application**

    ```bash
    python main.py
    ```

2. **Interact with the GUI**

    - **Enter Stock Ticker**: Type the stock ticker symbol in the provided entry field.
    - **Set Date Range**: Input the start and end dates or use the provided buttons to set the date range.
    - **Fetch Data**: Click the "Fetch Data" button to retrieve stock data and news.
    - **View Plot**: The graph will display the stock closing prices. Hover over the graph to see specific data points.
    - **News Articles**: Scroll through the news articles displayed below the plot.

## Code Overview

- `main.py`: The main application script.
  - **Functions**:
    - `fetch_and_plot()`: Retrieves stock data, plots it, and fetches news stories.
    - `fetch_news()`: Retrieves and displays news articles.
    - `set_date_range()`: Sets the date range for fetching stock data.
  - **GUI Components**:
    - **Input Frame**: For entering stock ticker and date range.
    - **Plot Frame**: Displays the interactive plot.
    - **News Frame**: Shows fetched news articles with images.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request with your changes. For major changes, please open an issue first to discuss what you would like to change.


---

Happy Analyzing!
