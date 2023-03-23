from flask import Flask, render_template, request, jsonify
from glob import glob

app = Flask(__name__)

def validate_card_data(card_data):
    errors = []

    if 'uuid' in card_data:
        errors.append("'uuid' is a special key. delete or rename this field")

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


if __name__ == '__main__':
    extra_files = glob('templates/*.*') + glob('static/*.*')
    app.run(debug=True, extra_files=extra_files)
