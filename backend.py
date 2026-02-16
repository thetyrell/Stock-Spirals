#!/usr/bin/env python3
"""
Stock Data Backend using vectorbt-style data structure
This simulates what vectorbt would provide for stock data
"""

from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

def generate_stock_data(symbol, days=252):
    """
    Generate realistic stock data similar to what vectorbt would provide.
    Uses geometric Brownian motion for price simulation.
    
    Args:
        symbol: Stock ticker symbol
        days: Number of trading days to generate
        
    Returns:
        Dictionary with stock data in vectorbt format
    """
    # Set seed based on symbol for consistent data per stock
    seed = sum(ord(c) for c in symbol)
    np.random.seed(seed)
    
    # Base parameters for different stocks
    stock_params = {
        'AAPL': {'base_price': 170, 'volatility': 0.25, 'drift': 0.0003},
        'GOOG': {'base_price': 140, 'volatility': 0.28, 'drift': 0.0002},
        'MSFT': {'base_price': 380, 'volatility': 0.23, 'drift': 0.0004},
        'TSLA': {'base_price': 240, 'volatility': 0.45, 'drift': 0.0001},
        'AMZN': {'base_price': 175, 'volatility': 0.30, 'drift': 0.0003},
        'META': {'base_price': 485, 'volatility': 0.32, 'drift': 0.0002},
        'NVDA': {'base_price': 880, 'volatility': 0.40, 'drift': 0.0005},
        'DEFAULT': {'base_price': 100, 'volatility': 0.25, 'drift': 0.0002}
    }
    
    params = stock_params.get(symbol.upper(), stock_params['DEFAULT'])
    
    # Generate dates (trading days only)
    end_date = datetime.now()
    dates = []
    current_date = end_date - timedelta(days=days * 1.4)  # Account for weekends
    while len(dates) < days:
        if current_date.weekday() < 5:  # Monday = 0, Friday = 4
            dates.append(current_date)
        current_date += timedelta(days=1)
    
    # Generate price series using geometric Brownian motion
    dt = 1  # daily time step
    prices = [params['base_price']]
    
    for i in range(1, days):
        # Random walk with drift
        random_shock = np.random.normal(0, 1)
        drift = params['drift'] * dt
        diffusion = params['volatility'] * random_shock * np.sqrt(dt)
        
        # Calculate next price
        price_change = prices[-1] * (drift + diffusion)
        new_price = prices[-1] + price_change
        
        # Ensure price doesn't go negative
        new_price = max(new_price, params['base_price'] * 0.3)
        prices.append(new_price)
    
    # Generate OHLCV data
    data = []
    for i, (date, close) in enumerate(zip(dates, prices)):
        # Generate realistic OHLC based on close
        daily_range = close * params['volatility'] * 0.1
        open_price = close + np.random.uniform(-daily_range, daily_range)
        high = max(open_price, close) + abs(np.random.uniform(0, daily_range))
        low = min(open_price, close) - abs(np.random.uniform(0, daily_range))
        volume = int(np.random.uniform(50000000, 150000000))
        
        data.append({
            'date': date.strftime('%Y-%m-%d'),
            'open': round(open_price, 2),
            'high': round(high, 2),
            'low': round(low, 2),
            'close': round(close, 2),
            'volume': volume
        })
    
    return {
        'symbol': symbol.upper(),
        'data': data,
        'stats': {
            'start_date': dates[0].strftime('%Y-%m-%d'),
            'end_date': dates[-1].strftime('%Y-%m-%d'),
            'trading_days': len(dates),
            'start_price': round(prices[0], 2),
            'end_price': round(prices[-1], 2),
            'total_return': round(((prices[-1] - prices[0]) / prices[0]) * 100, 2),
            'max_price': round(max(prices), 2),
            'min_price': round(min(prices), 2),
            'volatility': round(params['volatility'] * 100, 2)
        }
    }


@app.route('/api/stock/<symbol>', methods=['GET'])
def get_stock_data(symbol):
    """
    API endpoint to get stock data
    
    Query parameters:
        - days: Number of trading days (default: 252 = 1 year)
    """
    try:
        days = request.args.get('days', default=252, type=int)
        
        # Validate input
        if days < 5:
            days = 5
        elif days > 1260:  # Max 5 years
            days = 1260
        
        # Generate data
        stock_data = generate_stock_data(symbol, days)
        
        return jsonify({
            'success': True,
            'data': stock_data
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/stocks', methods=['POST'])
def get_multiple_stocks():
    """
    API endpoint to get multiple stocks at once
    
    JSON body:
        {
            "symbols": ["AAPL", "GOOG", "MSFT"],
            "days": 252
        }
    """
    try:
        data = request.get_json()
        symbols = data.get('symbols', [])
        days = data.get('days', 252)
        
        if not symbols:
            return jsonify({
                'success': False,
                'error': 'No symbols provided'
            }), 400
        
        results = {}
        for symbol in symbols:
            results[symbol] = generate_stock_data(symbol, days)
        
        return jsonify({
            'success': True,
            'data': results
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'version': '1.0',
        'backend': 'vectorbt-style'
    })


if __name__ == '__main__':
    print("=" * 60)
    print("Stock Data Backend Server")
    print("Using vectorbt-style data generation")
    print("=" * 60)
    print("\nAvailable endpoints:")
    print("  GET  /api/health")
    print("  GET  /api/stock/<symbol>?days=252")
    print("  POST /api/stocks (JSON: {symbols: [...], days: 252})")
    print("\nStarting server on http://localhost:5000")
    print("=" * 60)
    
    app.run(host='0.0.0.0', port=5000, debug=True)
