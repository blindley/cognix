from flask import Blueprint, render_template
import os

this_dir = os.path.dirname(os.path.abspath(__file__))
template_dir = os.path.join(this_dir, 'templates')
static_dir = os.path.join(this_dir, 'static')
ui = Blueprint('ui', __name__, template_folder=template_dir, static_folder=static_dir)

@ui.route('/card-editor')
def card_editor():
    return render_template('card_editor.html')

@ui.route('/data')
def display_data():
    return render_template('data.html')
