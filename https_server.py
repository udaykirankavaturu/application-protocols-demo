from flask import Flask
import ssl

app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>HTTPS Demo</h1><p>This is a simple HTTPS server using Flask.</p>'

if __name__ == '__main__':
    context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    context.load_cert_chain('cert.pem', 'key.pem')
    app.run(host='0.0.0.0', port=8443, ssl_context=context)
