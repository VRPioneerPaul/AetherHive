from flask import Flask, jsonify, render_template
import logging

LOGGER: logging.Logger = logging.getLogger("FlaskApp")

app = Flask(__name__)

@app.route('/')
def index():
    LOGGER.info('Rendering index.html')
    return render_template('index.html')

@app.route('/status')
def status():
    LOGGER.info('Returning status JSON')
    return jsonify()

@app.route('/about')
def about():
    LOGGER.info('Rendering about page')
    return "About page"

if __name__ == '__main__':
    LOGGER.info('Starting Flask app')
    app.run(debug=False, use_reloader=True)
