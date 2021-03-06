from flask import Flask, render_template
from flask_compress import Compress
import os, sys
import logging

def server_start(port,workdir):

    compress = Compress()
    app = Flask(__name__,template_folder=workdir+'/'+'webres',static_url_path='',static_folder=workdir+'/'+'webres')

    app.config['COMPRESS_MIN_SIZE'] = 0
    app.config['COMPRESS_LEVEL'] = 6
    app.config['COMPRESS_MIMETYPES'] = ['text/html', 'text/css', 'text/xml', 'application/json', 'application/javascript', 'application/octet-stream', 'image/svg+xml']

    compress.init_app(app)

    @app.after_request
    def add_header(response):
        if response.headers['Content-Type'] == "image/png":
            response.headers['Cache-Control'] = 'must-revalidate, public, max-age=86400'
        else:
            response.headers['Cache-Control'] = 'must-revalidate, public, max-age=-1'
        return response

    @app.route("/")
    def mainapp():
        return render_template('index.html')

    if not(__name__ == "__main__"):
        logging.getLogger('werkzeug').setLevel(logging.ERROR)
        app.logger.disabled = True

    while True:
        try:
            app.run(host='0.0.0.0', port=port)
        except Exception as e:
            sys.stdout.write('{}\n'.format(e))

if __name__ == "__main__":
    workdir = os.path.dirname(os.path.realpath(__file__))
    server_start(8000,workdir)
