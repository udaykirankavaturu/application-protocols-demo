# File: app_http3.py
from quart import Quart
import asyncio

# Initialize the Quart application
app = Quart(__name__)

@app.route('/')
async def index():
    """
    Renders the main page. The client-side code is identical,
    but it will be served over HTTP/3.
    """
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>HTTP/3 No-Blocking Demo</title>
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; line-height: 1.6; padding: 2em; max-width: 800px; margin: auto; background-color: #f4f7f9; }
            h1, h2, h3 { color: #333; }
            p { color: #555; }
            .container { background-color: #fff; padding: 2em; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }
            .controls, .results { margin-top: 1.5em; }
            button { font-size: 1em; padding: 0.6em 1.2em; margin: 0.5em 0.5em 0.5em 0; cursor: pointer; border: none; border-radius: 5px; color: white; background-color: #28a745; transition: background-color 0.3s; }
            button:hover { background-color: #218838; }
            button#clearBtn { background-color: #dc3545; }
            button#clearBtn:hover { background-color: #c82333; }
            #results-log { background-color: #e9ecef; margin-top: 1em; padding: 1em; border-radius: 5px; font-family: 'SF Mono', 'Courier New', monospace; font-size: 0.9em; height: 200px; overflow-y: auto; color: #495057; }
            #results-log div { margin-bottom: 0.5em; }
            strong { color: #007bff; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>HTTP/3 &amp; QUIC No-Blocking Demo</h1>
            <p>This demo is served over HTTP/3. Use your browser's developer tools (Network tab) to verify the protocol is <strong>h3</strong>.</p>
            
            <div class="controls">
                <h3>Controls</h3>
                <button id="demoBtn">Run Non-Blocking Demo</button>
                <button id="clearBtn">Clear Log</button>
            </div>

            <div class="results">
                <h3>Log</h3>
                <div id="results-log"></div>
            </div>
        </div>

        <script>
            const demoBtn = document.getElementById('demoBtn');
            const clearBtn = document.getElementById('clearBtn');
            const resultsLog = document.getElementById('results-log');

            function log(message) {
                const time = new Date().toLocaleTimeString();
                resultsLog.innerHTML += `<div>[${time}] ${message}</div>`;
                resultsLog.scrollTop = resultsLog.scrollHeight;
            }
            
            demoBtn.addEventListener('click', () => {
                log('--- Starting Demo ---');
                
                log('Sending request to /slow...');
                fetch('/slow')
                    .then(response => response.text())
                    .then(data => {
                        log('<strong>SUCCESS:</strong> Received response from /slow.');
                    });

                setTimeout(() => {
                    log('Sending request to /fast...');
                    fetch('/fast')
                        .then(response => response.text())
                        .then(data => {
                            log('<strong>SUCCESS:</strong> Received response from /fast. It was not blocked!');
                        });
                }, 100);
            });

            clearBtn.addEventListener('click', () => {
                resultsLog.innerHTML = '';
            });
        </script>
    </body>
    </html>
    """

@app.route('/slow')
async def slow_request():
    """
    Simulates a long-running task using asyncio.sleep for non-blocking delay.
    """
    print("Received /slow request. Processing will take 5 seconds...")
    await asyncio.sleep(5)
    print("Finished processing /slow request.")
    return "<h1>Slow Request Complete</h1>"

@app.route('/fast')
async def fast_request():
    """
    A quick endpoint that will respond immediately.
    """
    print("Received /fast request. Processing...")
    print("Finished processing /fast request.")
    return "<h1>Fast Request Complete</h1>"

# As before, we don't use app.run(). We use Hypercorn from the
# command line to get full HTTP/3 and QUIC support.