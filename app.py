from flask import Flask, render_template, request, jsonify
from sqlalchemy import MetaData, Table
from glob import glob
from card import add_card, engine, session
from uuid import uuid4

app = Flask(__name__)

def validate_card_data(card_data):
    errors = []

    card_uuid = str(uuid4())
    add_card(card_uuid, card_data)

    return errors if errors else None


@app.route('/')
def index():
    return render_template('card_editor.html')

@app.route('/process-card-data', methods=['POST'])
def process_json():
    card_data = request.json
    errors = validate_card_data(card_data)

    if errors:
        return jsonify(success=False, errors=errors)
    else:
        # Perform server-side processing on card_data as needed
        print(card_data)
        return jsonify(success=True)

@app.route('/data')
def display_data():
    metadata = MetaData()
    metadata.reflect(bind=engine)

    tables = {}
    for table_name in metadata.tables:
        table = Table(table_name, metadata, autoload=True, autoload_with=engine)
        result = session.query(table).all()
        keys = table.columns.keys()
        rows = [dict(zip(keys, row)) for row in result]
        tables[table_name] = rows

    return render_template('data.html', tables=tables)



if __name__ == '__main__':
    extra_files = glob('templates/*.*') + glob('static/*.*')
    app.run(debug=True, extra_files=extra_files)
