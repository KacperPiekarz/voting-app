from flask import Flask, jsonify, request, render_template
import redis
from .config import Config

app = Flask(__name__, template_folder='templates')
app.config.from_object(Config)

try:
    r = redis.Redis(host=app.config['REDIS_HOST'], port=app.config['REDIS_PORT'], decode_responses=True)
except:
    r = None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/vote', methods=['POST'])
def vote():
    if not r: return jsonify(msg="Brak bazy"), 503
    data = request.get_json()
    option = data.get('option')
    if option in app.config['VOTING_OPTIONS']:
        r.incr(f"vote:{option}")
        return jsonify(msg="OK")
    return jsonify(msg="Błąd"), 400

@app.route('/api/results', methods=['GET'])
def results():
    if not r: return jsonify(msg="Brak bazy"), 503
    wyniki = {opt: int(r.get(f"vote:{opt}") or 0) for opt in app.config['VOTING_OPTIONS']}
    return jsonify(wyniki)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)