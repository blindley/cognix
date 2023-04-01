from flask import Flask, render_template, request, jsonify
from glob import glob
import card
from api2 import api2

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(api2)

@app.route('/card-editor')
def card_editor():
    return render_template('card_editor.html')

@app.route('/data')
def display_data():
    tables = card.get_tables()
    return render_template('data.html', tables=tables)


def get_cards_handler(data):
    card_list = []
    for card_uuid in data:
        card_data = card.get_card_by_uuid(card_uuid)
        card_list.append(card_data)

    return card_list

def all_data_handler(data):
    tables = card.get_tables()
    return tables

def new_card_handler(data):
    result = card.add_card(None, data)
    if result["errors"]:
        return {"status": "error", "errors": result["errors"]}
    else:
        return {"status": "success", "uuid": result["uuid"]}


# Create a dictionary mapping request types to handlers
request_handlers = {
    "getCards": get_cards_handler,
    "allData": all_data_handler,
    "newCard": new_card_handler
}

@app.route('/api', methods=['POST'])
def process_requests():
    req_data = request.get_json()
    requests = req_data.get('requests', [])
    responses = []

    for req in requests:
        req_type = req.get('type')
        req_data = req.get('data')

        handler = request_handlers.get(req_type)

        if handler:
            response = handler(req_data)
        else:
            response = {"error": f"Unrecognized request type: {req_type}"}

        responses.append(response)

    return jsonify({"responses": responses})


if __name__ == '__main__':
    extra_files = glob('templates/*.*') + glob('static/*.*')
    app.run(debug=True, extra_files=extra_files)
