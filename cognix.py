from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

def validate_json(json_data):
    errors = []

    if 'uuid' in json_data:
        errors.append("'uuid' is a special key. delete or rename this field")

    return errors if errors else None


@app.route('/')
def index():
    return render_template('json_editor.html')

@app.route('/process-json', methods=['POST'])
def process_json():
    json_data = request.json
    errors = validate_json(json_data)

    if errors:
        return jsonify(success=False, errors=errors)
    else:
        # Perform server-side processing on json_data as needed
        print(json_data)
        return jsonify(success=True)


if __name__ == '__main__':
    app.run(debug=True)
