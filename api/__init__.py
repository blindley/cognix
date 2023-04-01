from flask import Blueprint, request, jsonify
import card

api = Blueprint('api', __name__)

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
    
def delete_cards_handler(data):
    try:
        card.delete_cards(data)
        return {"status": "success"}
    except Exception as e:
        return {"status": "error", "message": str(e)}

# Create a dictionary mapping request types to handlers
request_handlers = {
    "getCards": get_cards_handler,
    "allData": all_data_handler,
    "newCard": new_card_handler,
    "deleteCards": delete_cards_handler,
}

@api.route('/', methods=['POST'])
def index():
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
