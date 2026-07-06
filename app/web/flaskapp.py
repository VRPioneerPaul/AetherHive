from flask import Flask, jsonify, render_template
from .api.main import health

app = Flask(__name__)

@app.route('/')
def index():
    print('Rendering index.html')
    return render_template('index.html')

@app.route('/status')
def status():
    print('Returning status')
    return jsonify(health)

if __name__ == '__main__':
    print('Starting Flask app')
    app.run(debug=False, use_reloader=True)
