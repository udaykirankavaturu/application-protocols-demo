from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>HTTP/2 Demo</h1><p>This is a simple HTTP/2 server (served over HTTPS).</p>'

# This file is intended to be run with Hypercorn for HTTP/2 support
# Example: hypercorn http2_server:app --bind 0.0.0.0:8082 --certfile cert.pem --keyfile key.pem --h2
