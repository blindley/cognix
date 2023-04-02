from flask import Blueprint, render_template

ui = Blueprint('ui', __name__)

@ui.route('/card-editor')
def card_editor():
    return render_template('card_editor.html')

@ui.route('/data')
def display_data():
    return render_template('data.html')
