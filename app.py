from flask import Flask, render_template, request, jsonify
from glob import glob
import card

app = Flask(__name__)

@app.route('/card-editor', defaults={'card_uuid': None})
@app.route('/card-editor/<card_uuid>')
def card_editor(card_uuid):
    card_data = None
    if card_uuid:
        card_data = card.get_card_by_uuid(card_uuid)
    return render_template('card_editor.html', card_data=card_data, card_uuid=card_uuid)

@app.route('/submit-card', methods=['POST'])
def process_json():
    request_data = request.json
    card_uuid = request_data.get('uuid')
    card_data = request_data.get('cardData')

    errors = card.add_card(card_uuid, card_data)

    if errors:
        return jsonify(success=False, errors=errors)
    else:
        # Perform server-side processing on card_data as needed
        print(card_data)
        return jsonify(success=True)
    
@app.route('/search-cards', methods=['POST'])
def search_cards_route():
    search_dict = request.json
    matching_cards = card.search_cards(search_dict)
    results = [{'uuid': card.uuid, 'json': card.json} for card in matching_cards]
    return jsonify(results)

@app.route('/data')
def display_data():
    tables = card.get_tables()
    return render_template('data.html', tables=tables)

if __name__ == '__main__':
    extra_files = glob('templates/*.*') + glob('static/*.*')
    app.run(debug=True, extra_files=extra_files)
