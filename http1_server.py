from flask import Flask
import time

# Initialize the Flask application
app = Flask(__name__)

@app.route('/')
def index():
    """
    Renders the main page which explains the demo and provides an interactive
    way to observe Head-of-Line blocking using JavaScript.
    """
    # HTML for the main page with JS to demonstrate HOL blocking.
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Head-of-Line Blocking Demo</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; padding: 2em; max-width: 800px; margin: auto; background-color: #f4f7f9; }
            h1, h2, h3 { color: #333; }
            p { color: #555; }
            .container { background-color: #fff; padding: 2em; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            .controls, .results { margin-top: 1.5em; }
            button { font-size: 1em; padding: 0.6em 1.2em; margin: 0.5em 0.5em 0.5em 0; cursor: pointer; border: none; border-radius: 5px; color: white; background-color: #007bff; transition: background-color 0.3s; }
            button:hover { background-color: #0056b3; }
            button#clearBtn { background-color: #dc3545; }
            button#clearBtn:hover { background-color: #c82333; }
            #results-log { background-color: #e9ecef; margin-top: 1em; padding: 1em; border-radius: 5px; font-family: 'SF Mono', 'Courier New', monospace; font-size: 0.9em; height: 200px; overflow-y: auto; color: #495057; }
            #results-log div { margin-bottom: 0.5em; }
            strong { color: #28a745; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>HTTP/1.1 Head-of-Line Blocking Demo</h1>
            <p>This interactive demo shows how a single long-running request blocks subsequent requests on a single-threaded server.</p>
            
            <div class="controls">
                <h3>Controls</h3>
                <button id="demoBtn">Run HOL Blocking Demo</button>
                <button id="slowBtn">Request /slow (5s)</button>
                <button id="fastBtn">Request /fast (instant)</button>
                <button id="clearBtn">Clear Log</button>
            </div>

            <div class="results">
                <h3>Log</h3>
                <div id="results-log"></div>
            </div>
             <p><strong>To run the demo:</strong> Click the "Run HOL Blocking Demo" button. It will send a request to the slow endpoint, and then immediately to the fast endpoint. Observe the timestamps in the log to see the fast request being blocked.</p>
        </div>

        <script>
            const slowBtn = document.getElementById('slowBtn');
            const fastBtn = document.getElementById('fastBtn');
            const demoBtn = document.getElementById('demoBtn');
            const clearBtn = document.getElementById('clearBtn');
            const resultsLog = document.getElementById('results-log');

            function log(message) {
                const time = new Date().toLocaleTimeString();
                resultsLog.innerHTML += `<div>[${time}] ${message}</div>`;
                resultsLog.scrollTop = resultsLog.scrollHeight;
            }

            slowBtn.addEventListener('click', () => {
                log('Sending request to /slow...');
                fetch('/slow')
                    .then(response => response.text())
                    .then(data => {
                        log('<strong>SUCCESS:</strong> Received response from /slow.');
                    })
                    .catch(error => {
                        log(`<strong style="color:red;">ERROR:</strong> /slow request failed: ${error}`);
                    });
            });

            fastBtn.addEventListener('click', () => {
                log('Sending request to /fast...');
                fetch('/fast')
                    .then(response => response.text())
                    .then(data => {
                        log('<strong>SUCCESS:</strong> Received response from /fast.');
                    })
                    .catch(error => {
                        log(`<strong style="color:red;">ERROR:</strong> /fast request failed: ${error}`);
                    });
            });
            
            demoBtn.addEventListener('click', () => {
                log('--- Starting Demo ---');
                
                // First, send the slow request
                log('Sending request to /slow...');
                fetch('/slow')
                    .then(response => response.text())
                    .then(data => {
                        log('<strong>SUCCESS:</strong> Received response from /slow.');
                    });

                // A moment later, send the fast request
                setTimeout(() => {
                    log('Sending request to /fast...');
                    fetch('/fast')
                        .then(response => response.text())
                        .then(data => {
                            log('<strong>SUCCESS:</strong> Received response from /fast. Notice the completion time!');
                        });
                }, 100); // Fired 100ms after the slow request is initiated
            });

            clearBtn.addEventListener('click', () => {
                resultsLog.innerHTML = '';
            });
        </script>
    </body>
    </html>
    """

@app.route('/slow')
def slow_request():
    """
    This route simulates a long-running task.
    It will sleep for 5 seconds before returning a response.
    This is the request that will be at the "head of the line".
    """
    print("Received /slow request. Processing will take 5 seconds...")
    time.sleep(5)
    print("Finished processing /slow request.")
    return "<h1>Slow Request Complete</h1><p>This page was delayed for 5 seconds.</p>"

@app.route('/fast')
def fast_request():
    """
    This route should be very fast, but it will get blocked
    by any ongoing '/slow' request.
    """
    print("Received /fast request. Processing...")
    print("Finished processing /fast request.")
    return "<h1>Fast Request Complete</h1><p>This page loaded quickly.</p>"

if __name__ == '__main__':
    # The default Flask development server is single-threaded by default.
    # We explicitly set threaded=False to make this clear. This is what
    # allows for the head-of-line blocking demonstration.
    # In a production setup, you would use a WSGI server like Gunicorn or uWSGI
    # with multiple worker processes to handle concurrent requests.
    app.run(host='0.0.0.0', port=8081, threaded=False)
