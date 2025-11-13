from flask import Flask, jsonify
import yfinance as yf

app = Flask(__name__)

# Función para obtener datos de una acción con yfinance
def get_stock_data_yf(ticker):
    try:
        stock = yf.Ticker(ticker)
        # hist() devuelve los datos históricos. period="1d" nos da el del último día.
        hist = stock.history(period="1d")

        if hist.empty:
            raise Exception("No data found for ticker")

        # El formato de la moneda depende del ticker
        currency_symbol = '$' if '.' not in ticker or '.US' in ticker else '€'

        last_row = hist.iloc[-1]
        # Usamos el nombre corto de la compañía si está disponible
        stock_name = stock.info.get('shortName', ticker)

        return {
            "name": stock_name,
            "last": f"{last_row['Close']:.2f} {currency_symbol}",
            "high": f"{last_row['High']:.2f} {currency_symbol}",
            "low": f"{last_row['Low']:.2f} {currency_symbol}",
            "open": f"{last_row['Open']:.2f} {currency_symbol}",
            "volume": f"{last_row['Volume']:,}"
        }
    except Exception as e:
        print(f"Error getting data for {ticker}: {e}")
        return {
            "name": f"{ticker} (Error)",
            "last": "N/A", "high": "N/A", "low": "N/A", "open": "N/A", "volume": "N/A"
        }

@app.route('/stocks', methods=['GET'])
def get_all_stocks():
    # Tickers correctos para Yahoo Finance (con el sufijo .MC para Madrid)
    ibex_tickers = ["REP.MC", "TEF.MC", "SAN.MC", "BBVA.MC", "ITX.MC",
                    "IBE.MC", "ELE.MC", "NTGY.MC", "AMS.MC", "AENA.MC"]

    nasdaq_tickers = ["AAPL", "MSFT", "AMZN", "GOOGL", "META"]

    all_stocks_data = []

    # Obtener datos de acciones españolas
    for ticker in ibex_tickers:
        all_stocks_data.append(get_stock_data_yf(ticker))

    # Obtener datos de acciones de EE.UU.
    for ticker in nasdaq_tickers:
        all_stocks_data.append(get_stock_data_yf(ticker))

    return jsonify(all_stocks_data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
