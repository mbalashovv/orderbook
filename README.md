# Order Book Visualization

This project is an implementation of an order book (DOM) with a real-time visualization interface using Plotly Dash. The data is sourced from ByBit's open API, providing live and authentic market information.

![Endpoints](https://imgur.com/epy71O8.gif)

## Features
- **Real-time Data**: Continuously updated market data fetched from ByBit API.
- **All Market Pairs**: Automatically retrieves all available market pairs from the API.
- **Customizable Settings**: Easy to adjust settings.

## Requirements
- Python >= 3.12
- Dependencies listed in `pyproject.toml`

## Usage
1. Clone the repository.
2. Install dependencies using `poetry install`.
3. Run the application: `make run`.

## Settings

The application includes a range of configurable settings to tailor its behavior and display. Below is a detailed explanation of each:

### Application Settings
- **`APP_DEBUG`**: Enables or disables debug mode for development purposes.  
  *Default*: `True`  
- **`APP_PORT`**: Specifies the port where the Dash app runs.  
  *Default*: `8050`  
- **`APP_UPDATE_INTERVAL_MS`**: The interval (in milliseconds) at which the order book data updates.  
  *Default*: `3000` (3 seconds)

### API Configuration
- **`API_URL`**: The base URL for the ByBit API.  
  *Default*: `"https://api.bybit.com"`  
- **`API_ORDERS_LIMIT`**: Limits the number of orders fetched per request.  
  *Default*: `200`  
- **`API_ORDERS_CATEGORY`**: Defines the trading category (`spot`, `linear`, `inverse`, `option`).  
  *Default*: `"spot"`

### Order Book Settings
- **`ORDERBOOK_LEVELS_TO_SHOW`**: Number of price levels to display in the order book visualization.  
  *Default*: `10`  
- **`ORDERBOOK_AGGREGATION_LEVELS`**: Available price aggregation levels for grouping order book data.  
  *Default*: `["0.01", "0.1", "1", "10", "100"]`  
- **`ORDERBOOK_QUANTITY_PRECISION`**: Precision options for displaying order quantities.  
  *Default*: `["0", "1", "2", "3", "4"]`  
- **`ORDERBOOK_PRICE_PRECISION`**: Precision options for displaying prices.  
  *Default*: `["0", "1", "2", "3", "4"]`

### Customization Example
Adjust these settings in the configuration file to suit your specific requirements. For example:
- Set `APP_UPDATE_INTERVAL_MS` to `1000` for 1-second updates.
- Increase `ORDERBOOK_LEVELS_TO_SHOW` to visualize more price levels.

By tweaking these parameters, you can optimize the application for different datasets, user preferences, or system capabilities.
