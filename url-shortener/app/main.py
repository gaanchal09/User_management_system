from flask import Flask, request, jsonify, redirect, abort
from app.models import url_store
from app.utils import generate_short_code, is_valid_url

app = Flask(__name__)

@app.route('/')
def health_check():
    return jsonify({
        "status": "healthy",
        "service": "URL Shortener API"
    })

@app.route('/api/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({"error": "Missing URL"}), 400

    long_url = data['url']
    if not is_valid_url(long_url):
        return jsonify({"error": "Invalid URL"}), 400

    # Short code generation and collision check
    short_code = generate_short_code()
    while url_store.exists(short_code):
        short_code = generate_short_code()

    url_store.create(short_code, long_url)
    return jsonify({
        "short_code": short_code,
        "short_url": f"http://localhost:5000/{short_code}"
    }), 201

@app.route('/<short_code>', methods=['GET'])
def redirect_short_url(short_code):
    long_url = url_store.get_url(short_code)
    if long_url is None:
        abort(404)
    url_store.increment_click(short_code)
    return redirect(long_url)

@app.route('/api/stats/<short_code>', methods=['GET'])
def get_stats(short_code):
    metadata = url_store.get_metadata(short_code)
    if metadata is None:
        return jsonify({"error": "Not found"}), 404
    return jsonify(metadata)

@app.route('/api/health')
def api_health():
    return jsonify({
        "status": "ok",
        "message": "URL Shortener API is running"
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
