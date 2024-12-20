from flask import Flask, jsonify, request
from flask_cors import CORS
import yfinance as yf

app = Flask(__name__)
CORS(app)

stock_info = [
    {'code': '2330.TW', 'name': '台積電', 'sector': '電子股', 'tag': '高股利'},
    {'code': '2317.TW', 'name': '鴻海', 'sector': '電子股', 'tag': '中風險'},
    {'code': '2610.TW', 'name': '中華航空', 'sector': '航運股', 'tag': '高風險'},
    {'code': '2454.TW', 'name': '聯發科', 'sector': '電子股', 'tag': '高股利'},
    {'code': '2603.TW', 'name': '長榮', 'sector': '航運股', 'tag': '高股利'},
    {'code': '2882.TW', 'name': '國泰金', 'sector': '金融股', 'tag': '低風險'},
    {'code': '2002.TW', 'name': '中鋼', 'sector': '原物料', 'tag': '中風險'},
    {'code': '1101.TW', 'name': '台泥', 'sector': '水泥股', 'tag': '低風險'},
    {'code': '2891.TW', 'name': '中信金', 'sector': '金融股', 'tag': '高股利'},
    {'code': '6505.TW', 'name': '台塑化', 'sector': '原物料', 'tag': '中風險'},
    {'code': '2357.TW', 'name': '華碩', 'sector': '電子股', 'tag': '中風險'},
    {'code': '2408.TW', 'name': '南亞科', 'sector': '電子股', 'tag': '高風險'}
]

@app.route('/get_stock_data', methods=['GET'])
def get_stock_data():
    query = request.args.get('query', '').strip()  
    query_type = request.args.get('type', 'all')   
    
    results = []
    for stock in stock_info:
        try:
            ticker = yf.Ticker(stock['code'])
            data = ticker.history(period="1d", interval="1m")
            latest = data.iloc[-1] if not data.empty else {'Close': "N/A", 'Open': "N/A"}
            price = round(latest['Close'], 2) if latest['Close'] != "N/A" else "N/A"
            change = round(price - latest['Open'], 2) if price != "N/A" else "N/A"
            
            stock_data = {
                'name': stock['name'],
                'code': stock['code'],
                'sector': stock['sector'],
                'tag': stock['tag'],
                'price': price,
                'change': change
            }
            if query_type == 'all' or \
               (query_type == 'tag' and query == stock['tag']) or \
               (query_type == 'sector' and query == stock['sector']) or \
               (query_type == 'code' and query == stock['code']):
                results.append(stock_data)
        except Exception as e:
            print(f"Error fetching {stock['code']}: {e}")
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
