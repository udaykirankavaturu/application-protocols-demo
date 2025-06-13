# Application Protocols Demo: HTTP/1.1, HTTP/2, HTTP/3, and HTTPS

This repository demonstrates the features and drawbacks of HTTP/1.1, HTTP/2, HTTP/3, and HTTPS using simple servers and Docker. You can run and test each protocol locally.

## Table of Contents

- [Overview](#overview)
- [Features & Drawbacks](#features--drawbacks)
- [How to Use](#how-to-use)
  - [HTTP/1.1 Demo](#http11-demo)
  - [HTTP/2 Demo](#http2-demo)
  - [HTTPS Demo](#https-demo)
  - [HTTP/3 Demo](#http3-demo)
- [Testing](#testing)
- [Cleanup](#cleanup)

## Overview

- **HTTP/1.1**: The classic protocol, supports persistent connections but only one request per connection at a time.
- **HTTP/2**: Multiplexes multiple requests over a single connection, header compression, server push.
- **HTTP/3**: Uses QUIC (UDP-based), faster connection setup, improved multiplexing, better for unreliable networks.
- **HTTPS**: HTTP over TLS, encrypts traffic for security.

## Features & Drawbacks

| Protocol | Features                                      | Drawbacks                                      |
| -------- | --------------------------------------------- | ---------------------------------------------- |
| HTTP/1.1 | Simple, widely supported                      | Head-of-line blocking, no multiplexing         |
| HTTP/2   | Multiplexing, header compression, server push | More complex, requires TLS in browsers         |
| HTTP/3   | Uses QUIC, faster, better multiplexing        | Newer, not supported everywhere, UDP issues    |
| HTTPS    | Encryption, privacy, integrity                | Certificate management, slightly more overhead |

## How to Use

### Prerequisites

- [Docker](https://www.docker.com/get-started) installed
- [Python 3.8+](https://www.python.org/downloads/) installed
- [pip](https://pip.pypa.io/en/stable/)

---

### HTTP/1.1 Demo

1. Install dependencies:
   ```sh
   pip3 install flask
   ```
2. Run the server:
   ```sh
   python3 http1_server.py
   ```
3. Visit [http://localhost:8081](http://localhost:8081)

---

### HTTP/2 Demo

1. Install dependencies:
   ```sh
   pip3 install flask hypercorn
   ```
2. Run the server:
   ```sh
   /Library/Frameworks/Python.framework/Versions/3.12/bin/hypercorn http2_server:app --bind 0.0.0.0:8082 --certfile cert.pem --keyfile key.pem
   ```
3. Visit [https://localhost:8082](https://localhost:8082) (accept self-signed cert)

---

### HTTPS Demo

1. Generate a self-signed certificate (if not present):
   ```sh
   openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"
   ```
2. Run the HTTPS server:
   ```sh
   python3 https_server.py
   ```
3. Visit [https://localhost:8443](https://localhost:8443) (accept self-signed cert)

---

### HTTP/3 Demo (QUIC)

1. Build and run the Caddy server (HTTP/3 enabled) using Docker:
   ```sh
   docker compose up --build
   ```
2. Visit [https://localhost:8444](https://localhost:8444) (accept self-signed cert)

---

## Testing

- Use your browser or `curl`:
  - HTTP/1.1: `curl -v http://localhost:8081`
  - HTTP/2: `curl -vk --http2 https://localhost:8082`
  - HTTPS: `curl -vk https://localhost:8443`
  - HTTP/3: `curl -vk --http3 https://localhost:8444`

## Cleanup

- Stop Python servers with `Ctrl+C`.
- Stop Docker containers:
  ```sh
  docker compose down
  ```

---

## Notes

- Self-signed certificates are used for demo purposes. Browsers will show a warning.
- HTTP/3 requires a browser or curl with HTTP/3 support.

---

## License

See [LICENSE](LICENSE).
