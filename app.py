from flask import Flask, render_template
from glob import glob
import card
from api import api

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(api, url_prefix='/api')

@app.route('/card-editor')
def card_editor():
    return render_template('card_editor.html')

@app.route('/data')
def display_data():
    tables = card.get_tables()
    return render_template('data.html', tables=tables)

if __name__ == '__main__':
    extra_files = glob('templates/*.*') + glob('static/*.*')
    app.run(debug=True, extra_files=extra_files)
