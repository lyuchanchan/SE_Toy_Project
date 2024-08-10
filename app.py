import requests
from flask import Flask, request, render_template, jsonify
import sqlite3
import os

app = Flask(__name__)
app.secret_key = 'your_secret_key'

API_KEY = os.getenv('SEOUL_SUBWAY_API_KEY', '735051707268736335374741514976')

line_mapping = {
    "1001": "1호선",
    "1002": "2호선",
    "1003": "3호선",
    "1004": "4호선",
    "1005": "5호선",
    "1006": "6호선",
    "1007": "7호선",
    "1008": "8호선",
    "1009": "9호선",
    "1063": "경의중앙선",
    "1065": "공항철도",
    "1067": "경춘선",
    "1075": "수인분당선",
    "1077": "신분당선",
    "1091": "자기부상철도"
}

def init_db():
    conn = sqlite3.connect('favorites.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS favorites
                  (id INTEGER PRIMARY KEY AUTOINCREMENT, line TEXT, station TEXT)''')
    conn.commit()
    conn.close()

def add_favorite(line, station):
    station_with_suffix = f"{station}역" if not station.endswith("역") else station
    conn = sqlite3.connect('favorites.db')
    c = conn.cursor()
    c.execute('INSERT INTO favorites (line, station) VALUES (?, ?)', (line, station_with_suffix))
    conn.commit()
    conn.close()

def get_favorites():
    conn = sqlite3.connect('favorites.db')
    c = conn.cursor()
    c.execute('SELECT line, station FROM favorites')
    favorites = c.fetchall() 
    conn.close()
    return favorites

def get_lines():
    return list(line_mapping.values())

@app.route('/')
def home():
    lines = get_lines()
    favorites = get_favorites()
    formatted_favorites = [(line, f"{station}") for line, station in favorites]
    return render_template('index.html', lines=lines, favorites=formatted_favorites)

@app.route('/search', methods=['POST'])
def search():
    line = request.form['line']
    station = request.form['station']

    if line not in line_mapping.values():
        return jsonify({'status': 'error', 'message': f"{line}은(는) 유효한 호선이 아닙니다."})

    url = f"http://swopenAPI.seoul.go.kr/api/subway/{API_KEY}/json/realtimeStationArrival/0/5/{station}"
    response = requests.get(url)
    data = response.json()

    if 'errorMessage' in data and data['errorMessage']['code'] == 'INFO-200':
        return jsonify({'status': 'error', 'message': f"{station}역 정보를 찾을 수 없습니다."})

    arrivals = data.get('realtimeArrivalList', [])
    up_arrivals = []
    down_arrivals = []

    for arrival in arrivals:
        subway_id = str(arrival.get('subwayId'))
        arrival['subwayLine'] = line_mapping.get(subway_id, subway_id)
        
        if arrival['subwayLine'] == line:
            if '상행' in arrival['updnLine']:
                up_arrivals.append(arrival)
            elif '하행' in arrival['updnLine']:
                down_arrivals.append(arrival)

    return render_template('search_results.html', station=station, up_arrivals=up_arrivals, down_arrivals=down_arrivals, line=line)

@app.route('/add_to_favorites', methods=['POST'])
def add_to_favorites():
    line = request.form['line']
    station = request.form['station']

    favorites = get_favorites()
    station_with_suffix = f"{station}역" if not station.endswith("역") else station
    if (line, station_with_suffix) not in favorites:
        add_favorite(line, station)
        return jsonify({'status': 'success', 'message': f"{station} ({line})이(가) 즐겨찾기에 추가되었습니다."})
    else:
        return jsonify({'status': 'info', 'message': f"{station} ({line})은(는) 이미 즐겨찾기에 추가되어 있습니다."})

@app.route('/seoul_transport')
def seoul_transport():
    return "서울 지하철 노선도 페이지"

if __name__ == '__main__':
    init_db()
    app.run(host='0.0.0.0', debug=True)
