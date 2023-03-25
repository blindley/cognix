from flask import Flask, render_template, request, jsonify
from glob import glob
import card
from uuid import uuid4

app = Flask(__name__)

def submit_card(card_data):
    errors = []

    card_uuid = str(uuid4())
    card.add_card(card_uuid, card_data)

    return errors if errors else None

@app.route('/card-editor')
def index():
    return render_template('card_editor.html')

@app.route('/process-card-data', methods=['POST'])
def process_json():
    card_data = request.json
    errors = submit_card(card_data)

    if errors:
        return jsonify(success=False, errors=errors)
    else:
        # Perform server-side processing on card_data as needed
        print(card_data)
        return jsonify(success=True)

@app.route('/data')
def display_data():
    tables = card.get_tables()
    return render_template('data.html', tables=tables)

if __name__ == '__main__':
    extra_files = glob('templates/*.*') + glob('static/*.*')
    app.run(debug=True, extra_files=extra_files)
