from flask import Blueprint, render_template
import os

template_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'templates')
ui = Blueprint('ui', __name__, template_folder=template_dir)

@ui.route('/card-editor')
def card_editor():
    return render_template('card_editor.html')

@ui.route('/data')
def display_data():
    return render_template('data.html')
