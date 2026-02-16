# Spiral Stock Chart with vectorbt Backend

This project visualizes stock data in an interactive 3D spiral chart using Three.js for the frontend and a Flask backend that provides data in a vectorbt-style format.

## Project Structure

```
.
├── backend.py              # Flask server providing stock data API
├── SpiralGrok_Updated.html # Updated frontend with backend integration
└── README.md              # This file
```

## Features

- **3D Spiral Visualization**: Interactive 3D chart showing stock price history in a spiral pattern
- **vectorbt-style Backend**: Flask API that generates realistic stock data using geometric Brownian motion
- **Multiple Stocks**: Compare up to 3 stocks simultaneously
- **Time Periods**: View data from 1 week to 5 years
- **Interactive Controls**: Drag to rotate the 3D visualization
- **Automatic Fallback**: Uses simulated data if backend is unavailable

## Setup Instructions

### Requirements

The backend requires:
- Python 3.x
- Flask
- Flask-CORS
- NumPy
- Pandas

### Installation

1. **Install Python dependencies:**

```bash
pip install flask flask-cors numpy pandas
```

### Running the Application

1. **Start the backend server:**

```bash
python3 backend.py
```

The server will start on `http://localhost:5000`

You should see:
```
============================================================
Stock Data Backend Server
Using vectorbt-style data generation
============================================================

Available endpoints:
  GET  /api/health
  GET  /api/stock/<symbol>?days=252
  POST /api/stocks (JSON: {symbols: [...], days: 252})

Starting server on http://localhost:5000
============================================================
```

2. **Open the frontend:**

Simply open `SpiralGrok_Updated.html` in your web browser.

Note: If you're running this locally, you may need to serve the HTML file through a local server to avoid CORS issues. You can use Python's built-in HTTP server:

```bash
python3 -m http.server 8080
```

Then visit `http://localhost:8080/SpiralGrok_Updated.html`

## Usage

1. **Enter Stock Symbols**: Type stock ticker symbols (e.g., AAPL, GOOG, MSFT) in the input fields
2. **Select Time Period**: Use the slider to choose from 1 week to 5 years
3. **Load Data**: Click "Load Stock Data" to fetch and visualize the data
4. **Interact**: Drag to rotate the 3D visualization

### Backend Status

The frontend will display the backend connection status:
- **Green**: "Backend connected ✓" - Using data from the backend
- **Red**: "Backend offline - using simulated data" - Using fallback simulated data

## API Documentation

### Health Check
```
GET /api/health
```

Returns server status and version information.

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0",
  "backend": "vectorbt-style"
}
```

### Get Single Stock Data
```
GET /api/stock/<symbol>?days=252
```

**Parameters:**
- `symbol`: Stock ticker symbol (e.g., AAPL)
- `days`: Number of trading days (default: 252, min: 5, max: 1260)

**Response:**
```json
{
  "success": true,
  "data": {
    "symbol": "AAPL",
    "data": [
      {
        "date": "2024-02-16",
        "open": 170.25,
        "high": 172.50,
        "low": 169.80,
        "close": 171.50,
        "volume": 85000000
      },
      ...
    ],
    "stats": {
      "start_date": "2024-02-16",
      "end_date": "2025-02-16",
      "trading_days": 252,
      "start_price": 170.00,
      "end_price": 175.50,
      "total_return": 3.24,
      "max_price": 180.00,
      "min_price": 165.00,
      "volatility": 25.00
    }
  }
}
```

### Get Multiple Stocks Data
```
POST /api/stocks
Content-Type: application/json
```

**Request Body:**
```json
{
  "symbols": ["AAPL", "GOOG", "MSFT"],
  "days": 252
}
```

**Response:**
```json
{
  "success": true,
  "data": {
    "AAPL": { ... },
    "GOOG": { ... },
    "MSFT": { ... }
  }
}
```

## Data Generation

The backend uses **geometric Brownian motion** to generate realistic stock price movements. Each stock has unique parameters:

- **Base Price**: Starting price point
- **Volatility**: Daily price fluctuation (sigma)
- **Drift**: Long-term trend (mu)

Supported stocks with custom parameters:
- AAPL, GOOG, MSFT, TSLA, AMZN, META, NVDA
- Any other symbol will use default parameters

## Troubleshooting

### Backend Not Connecting

1. Make sure the backend is running on port 5000
2. Check that Flask and dependencies are installed
3. Verify no firewall is blocking port 5000
4. The frontend will automatically fall back to simulated data

### CORS Issues

If you see CORS errors in the browser console:
1. Ensure Flask-CORS is installed
2. Try serving the HTML through a local web server
3. Check browser console for specific error messages

### Missing Data

If stocks show "Simulated" instead of "vectorbt":
1. Verify the backend is running
2. Check the backend status indicator in the UI
3. Look at browser console for network errors

## Customization

### Adding New Stocks

Edit `backend.py` and add your stock to the `stock_params` dictionary:

```python
stock_params = {
    'NEWSTOCK': {
        'base_price': 100,
        'volatility': 0.25,
        'drift': 0.0003
    },
    ...
}
```

### Changing Colors

Edit the `stockColors` array in `SpiralGrok_Updated.html`:

```javascript
var stockColors = [0x667eea, 0x10b981, 0xf59e0b]; // RGB hex colors
```

### Adjusting Visualization

Modify these parameters in the HTML:
- `radius = 10 + stockIndex * 3`: Distance between spiral tracks
- `Math.PI * 6`: Number of spiral rotations
- `normalizedPrice * 30`: Vertical scale

## Technical Details

### Frontend (SpiralGrok_Updated.html)
- **Three.js**: 3D rendering
- **WebGL**: Hardware-accelerated graphics
- **Responsive Design**: Adapts to window size

### Backend (backend.py)
- **Flask**: Web framework
- **NumPy**: Numerical computations
- **Pandas**: Data structures
- **Geometric Brownian Motion**: Realistic price generation

## License

This project is provided as-is for educational and demonstration purposes.

## Notes

- This is a demonstration/educational tool
- Stock data is simulated and not real market data
- For production use with real data, integrate with actual financial APIs (Alpha Vantage, Yahoo Finance, etc.)
- The vectorbt library itself provides much more functionality for backtesting and analysis
