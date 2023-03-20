from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('json_editor.html')

@app.route('/process-json', methods=['POST'])
def process_json():
    json_data = request.json
    # Perform server-side processing on json_data as needed
    print(json_data)
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(debug=True)
