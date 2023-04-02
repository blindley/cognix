from flask import Flask, render_template
from glob import glob
import logging
from api import api
from ui import ui

app = Flask(__name__)
app.url_map.strict_slashes = False
app.register_blueprint(api, url_prefix='/api')
app.register_blueprint(ui)

log_format = "[%(asctime)s] %(levelname)s in %(module)s: %(message)s"
logging.basicConfig(level=logging.DEBUG, format=log_format)

if __name__ == '__main__':
    extra_files = glob('templates/*.*') + glob('static/*.*')
    app.run(debug=True, extra_files=extra_files)
