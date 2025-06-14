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

- [Python 3.8+](https://www.python.org/downloads/) installed
- caddy server installed

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
   pip3 install quart hypercorn h2
   ```
2. Generate certificates:
   ```sh
   openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
   ```
3. Run the server:
   ```sh
   /Library/Frameworks/Python.framework/Versions/3.12/bin/hypercorn --certfile cert.pem --keyfile key.pem http2_server:app --bind "0.0.0.0:8081"
   ```
4. Visit [https://localhost:8081](https://localhost:8081) (accept self-signed cert)

---

### HTTP3 Demo

1. Install dependencies

```sh
pip3 install quart hypercorn aioquic
```

2. Generate certificates:

```sh
openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365
```

3. Run server

```
/Library/Frameworks/Python.framework/Versions/3.12/bin/hypercorn http3_server:app --bind "0.0.0.0:8081" --quic-bind "0.0.0.0:8081" --certfile cert.pem --keyfile key.pem
```

4. Visit [https://localhost:8081](https://localhost:8081) (accept self-signed cert)

## License

See [LICENSE](LICENSE).
