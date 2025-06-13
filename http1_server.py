from flask import Flask
app = Flask(__name__)

@app.route('/')
def index():
    return '<h1>HTTP/1.1 Demo</h1><p>This is a simple HTTP/1.1 server.</p>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8081)
