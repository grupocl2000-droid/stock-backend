from flask import Flask, jsonify, request
import yfinance as yf
import pandas as pd

app = Flask(__name__)

def get_stock_data(symbol):
    try:
        stock = yf.Ticker(symbol)
        # hist para 2 días para tener cierre previo
        hist = stock.history(period="2d")

        if hist.empty:
            # Devuelve una estructura con nulos si no hay datos
            return {
                "currentPrice": None,
                "previousClosePrice": None,
                "high": None,
                "low": None,
                "open": None,
                "volume": None,
                "timestamp": None
            }

        last_row = hist.iloc[-1]
        # El cierre previo es el de la penúltima fila, si existe
        prev_close = hist.iloc[-2]['Close'] if len(hist) > 1 else None
        
        # El timestamp es la fecha del último dato, en segundos
        timestamp = int(hist.index[-1].timestamp())

        return {
            "currentPrice": last_row['Close'],
            "previousClosePrice": prev_close,
            "high": last_row['High'],
            "low": last_row['Low'],
            # yfinance devuelve 'Open', lo mapeamos a 'open'
            "open": last_row['Open'],
            "volume": last_row['Volume'],
            "timestamp": timestamp
        }
    except Exception as e:
        print(f"Error getting data for {symbol}: {e}")
        # Si hay un error, devuelve la misma estructura con nulos
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
