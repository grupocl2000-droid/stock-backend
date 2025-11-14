from flask import Flask, jsonify, request
import yfinance as yf
import pandas as pd

app = Flask(__name__)

def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        # yfinance puede devolver un diccionario simple si el símbolo no es válido.
        # Comprobamos que 'regularMarketTime' exista para asegurar que tenemos datos válidos.
        if 'regularMarketTime' not in info or info['regularMarketTime'] is None:
            return {
                "currentPrice": None,
                "previousClosePrice": None,
                "high": None,
                "low": None,
                "open": None,
                "volume": None,
                "timestamp": None
            }

        return {
            "currentPrice": info.get('regularMarketPrice'),
            "previousClosePrice": info.get('regularMarketPreviousClose'),
            "high": info.get('regularMarketDayHigh'),
            "low": info.get('regularMarketDayLow'),
            "open": info.get('regularMarketOpen'),
            "volume": info.get('regularMarketVolume'),
            "timestamp": info.get('regularMarketTime')
        }
    except Exception as e:
        print(f"Error getting data for {symbol}: {e}")
        return {
            "currentPrice": None,
            "previousClosePrice": None,
            "high": None,
            "low": None,
            "open": None,
            "volume": None,
            "timestamp": None
        }

@app.route('/quote', methods=['GET'])
def get_quote():
    # Leemos el símbolo del parámetro en la URL (ej: /quote?symbol=TEF.MC)
    symbol = request.args.get('symbol')
    if not symbol:
        return jsonify({"error": "El parámetro 'symbol' es obligatorio"}), 400

    data = get_stock_data(symbol)
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
